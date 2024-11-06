from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Order
from products.models import Product
from customers.models import Customer
from .serializers import orderSerializer
import pika
import json

# Helper function to publish messages to RabbitMQ
def publish_to_queue(queue, exchange, routing_key, data):
    #error handler
    try:
        #connecting to the rabbitMQ server using pika library
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
            host='10.204.4.76',
            credentials=pika.PlainCredentials('anand', '2004anand'))
        )
        channel = connection.channel()
        
        # Ensure queue exists
        channel.queue_declare(queue=queue, durable=True)
        
        # Publish the message
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
        )
        print(f"Published to {queue}: {data}")
    except Exception as e:
        print(f"Error publishing message: {str(e)}")
    finally:
        if connection:
            connection.close()

class orderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = orderSerializer

    def perform_create(self, serializer):
        #Override to validate, calculate total amount, and send to RabbitMQ.
        product_ids = self.request.data.get('products')
        customer_id = self.request.data.get('customer')

        # Validate customer
        customer = get_object_or_404(Customer, id = customer_id)

        # Validate products
        products = [get_object_or_404(Product, id = pid) for pid in product_ids]

        # Calculate total amount
        total_amount = sum(product.price for product in products)

        #Calculate total time to take 
        minutes = 0
        for product in products:
            minutes += product.minutesToTake
        
        # Save the order
        order = serializer.save(customer = customer, total_amount = total_amount)
        order.products.set(products)

        # Prepare message data to send order queue
        order_data = {
            "event": "order_created",
            "order_id": order.id,
            "customer_id": customer.id,
            "products": [product.id for product in products],
            "total_amount": total_amount,
            "status": order.status,
            "minutesToTake": minutes,
        }

        # Publish to RabbitMQ
        publish_to_queue('order-queue', 'order_exchange', 'order_routing_key', order_data)

class orderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = orderSerializer

    def perform_update(self, serializer):
        # Retrieve the original order (before update)
        original_order = self.get_object()
        previous_total_amount = original_order.total_amount
        #Update the order 
        order = serializer.save()

        product_ids = self.request.data.get('products')

        # Validate products
        products = [get_object_or_404(Product, id = pid) for pid in product_ids]

        #Calculate total time to take
        minutes = 0
        for product in products:
            minutes += product.minutesToTake

        # Calculate total amount
        total_amount = sum(product.price for product in products)

        refund_amount = 0
        extra_payment_amount = 0

        if total_amount >= previous_total_amount:
            extra_payment_amount = total_amount - previous_total_amount
        else:
            refund_amount = previous_total_amount - total_amount

        # Prepare message data
        order_data = {
            "event": "order_updated",
            "order_id": order.id,
            "customer_id": order.customer.id,
            "products": [product.id for product in order.products.all()],
            "total_amount": order.total_amount,
            "status": order.status,
            "minutesToTake": minutes,
            "refund": refund_amount,
            "extraPayment": extra_payment_amount
        }

        # Publish to RabbitMQ
        publish_to_queue('order-queue', 'order_exchange', 'order_routing_key', order_data)