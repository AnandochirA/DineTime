import pika
import json
import requests

def process_request(request):
    customerID = request.get('customer_id')
    action = request.get('action')
    value = request.get('value')

    try:
        consumer_response = requests.get(f'http://127.0.0.1:8000/api/customer/customers/{customerID}/')
        consumer_response.raise_for_status()  
        data = consumer_response.json()
        print("Customer Data:", data)

        if action == 'deposit':
            if value < 0:
                return {"status": "error", "message": "Deposit value must be non-negative."}
            data['balance'] += value
            put_response = requests.put(f'http://127.0.0.1:8000/api/customer/customers/{customerID}/', json=data)
            put_response.raise_for_status()
            print("Successfully updated customer data:", put_response.json())
            return {"status": "success", "message": "Deposit successful."}

        elif action == 'withdraw':
            if value < 0:
                return {"status": "error", "message": "Withdrawal value must be non-negative."}
            if value <= data['balance']:
                data['balance'] -= value
                put_response = requests.put(f'http://127.0.0.1:8000/api/customer/customers/{customerID}/', json=data)
                put_response.raise_for_status()
                print("Successfully updated customer data:", put_response.json())
                return {"status": "success", "message": "Withdrawal successful."}
            else:
                return {"status": "error", "message": "Insufficient funds."}

        else:
            return {"status": "error", "message": "Invalid action."}

    except requests.exceptions.RequestException as e:
        print("Error during HTTP request:", e)
        return {"status": "error", "message": "Failed to process request."}

def on_request(ch, method, properties, body):
    request = json.loads(body)

    response = process_request(request)

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_rpc_server():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='10.204.4.76',
                credentials=pika.PlainCredentials('anand', '2004anand')
            )
        )
        channel = connection.channel()

        rpc_queue = 'balance-queue'  
        channel.queue_declare(queue=rpc_queue, durable=True)

        channel.basic_consume(queue=rpc_queue, on_message_callback=on_request)

        print("Balance Server is waiting for requests...")
        channel.start_consuming()
    except Exception as e:
        print(f"Error in RPC server: {e}")

if __name__ == "__main__":
    start_rpc_server()
