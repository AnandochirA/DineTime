import pika
import json
import uuid

def send_request(action, customer_id, value):
    correlation_id = str(uuid.uuid4())
    request = {
        'action': action,
        'customer_id': customer_id,
        'value': value
    }

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

        result = channel.queue_declare(queue='', exclusive=True)
        response_queue = result.method.queue

        def on_response(ch, method, properties, body):
            if properties.correlation_id == correlation_id:
                print("Received response:", body.decode())
                ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=response_queue, on_message_callback=on_response)

        # Publish the request to the queue
        channel.basic_publish(
            exchange='',
            routing_key=rpc_queue,
            properties=pika.BasicProperties(
                reply_to=response_queue,
                correlation_id=correlation_id
            ),
            body=json.dumps(request)
        )
        print(f"Sent request: {request}")

        while True:
            channel.connection.process_data_events()
    except Exception as e:
        print(f"Error sending request: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    action = 'deposit' 
    customer_id = '2' 
    value = 100  
    send_request(action, customer_id, value)
