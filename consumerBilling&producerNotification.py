import pika
import requests
import json

# RabbitMQ configuration
BILLING_QUEUE = 'billing-queue'
NOTIFICATION_QUEUE = 'notification-queue'

NOTIFICATION_EXCHANGE = 'notification_exchange'  
def send_to_notification_queue(channel, customer_id, order_id, message):
    notification_data = {
        "customer_id": customer_id,
        "order_id": order_id,
        "message": message
    }

    channel.basic_publish(
        exchange=NOTIFICATION_EXCHANGE,  
        routing_key='',  
        body=json.dumps(notification_data),
        properties=pika.BasicProperties(
            delivery_mode=2  
        )
    )
    print(f"Notification sent to fanout exchange: {notification_data}")

def callback(ch, method, properties, body):
    billing_data = json.loads(body)
    print("Received billing data:", billing_data)

    # Extract required fields from the message
    customer_id = billing_data.get("customer_id")
    order_id = billing_data.get("order_id") 
    event = billing_data.get("event")

    if customer_id is None or order_id is None:
        print("Missing customer_id or order_id in the billing data:", billing_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message
        return 

    try:
        # Fetch the current customer data
        consumer_response = requests.get(
            f'http://127.0.0.1:8000/api/customer/customers/{customer_id}/'
        )
        data = consumer_response.json()

        if consumer_response.status_code == 200:
            print(f"Processing event: {event} for customer {customer_id}")
            total_amount = billing_data.get("total_amount")

            if event == "order_created":
                if data['balance'] >= total_amount:
                    data['balance'] -= total_amount
                    message = f"Order {order_id} created successfully! Balance is {data['balance']}."
                else:
                    message = f"Insufficient balance for customer {customer_id}."
                    print(message)

            elif event == "order_updated":
                extra_payment = billing_data.get("extra_payment")
                refund = billing_data.get("refund")

                if extra_payment > 0:
                    if extra_payment <= data['balance']:
                        data['balance'] -= extra_payment
                        message = f"Extra payment for order {order_id} processed successfully! Balance is {data['balance']}."
                    else:
                        message = f"Insufficient balance for extra payment by customer {customer_id}."

                elif refund > 0:
                    data['balance'] += refund
                    message = f"Refund for order {order_id} processed successfully! Balance is {data['balance']}."

            
            put_response = requests.put(
                f'http://127.0.0.1:8000/api/customer/customers/{customer_id}/',
                json = data
            )

            if put_response.status_code == 200:
                print("Successfully updated customer data:", put_response.json())
            else:
                print("Error updating customer data:", put_response.status_code, put_response.text)

            send_to_notification_queue(ch, customer_id, order_id, message)

        else:
            print("Error fetching customer data:", consumer_response.status_code, consumer_response.text)

    except Exception as e:
        print("Exception occurred while processing:", e)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='10.204.4.76',
            credentials=pika.PlainCredentials('anand', '2004anand')
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue=BILLING_QUEUE, durable=True)
    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

    channel.basic_consume(queue=BILLING_QUEUE, on_message_callback=callback)

    print('Waiting for messages in the billing queue...')
    channel.start_consuming()

if __name__ == '__main__':
    main()
