import pika
import requests
import json

# RabbitMQ configuration
BILLING_QUEUE = 'billing-queue'

def callback(ch, method, properties, body):
    billing_data = json.loads(body)

    # Fetch specific consumer data from REST API
    consumer_response = requests.get(f'http://127.0.0.1:8000/api/customer/customers/{billing_data["customer_id"]}/')

    if consumer_response.status_code == 200:
        consumer_data = consumer_response.json()

        # Implement billing logic
        if consumer_data['balance'] >= billing_data['total_amount']:
            # Deduct amount, update database, etc.
            consumer_data['balance'] -= billing_data['total_amount']
            # Send updated data back to the API
            update_response = requests.put(
                f'http://127.0.0.1:8000/api/customer/customers/{consumer_data["id"]}/', 
                json=consumer_data  # Include the updated data in the body
            )
            if update_response.status_code == 200:
                print(f"Billing successful for customer {consumer_data['name']}. Amount deducted: {billing_data['total_amount']}")
            else:
                print(f"Failed to update customer balance: {update_response.status_code}")
        else:
            print(f"Insufficient balance for customer {consumer_data['name']}.")
    else:
        print(f"Failed to fetch consumer data: {consumer_response.status_code}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='10.204.4.76',
            credentials=pika.PlainCredentials('anand', '2004anand')
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue=BILLING_QUEUE, durable=True)
    # Set up subscription to the queue
    channel.basic_consume(queue=BILLING_QUEUE, on_message_callback=callback)

    print('Waiting for messages in the billing queue...')
    channel.start_consuming()

if __name__ == '__main__':
    main()