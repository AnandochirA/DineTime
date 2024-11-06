import { connect } from 'amqplib';

const BILLING_QUEUE = 'billing-queue';

async function handleOrder(billingData) {
    console.log("Received order:", billingData);

    
    // Check if the order status is completed
    if (orderData.status === 'completed') {
        

        // Publish to billing queue
        channel.sendToQueue(BILLING_QUEUE, Buffer.from(JSON.stringify(billingData)), { persistent: true });
        console.log("Sent billing data to billing-queue:", billingData);
    }
}

async function consumeOrders() {
    try {
        // Connect to RabbitMQ
        const connection = await connect('amqp://your-rpi-ip-address');
        const channel = await connection.createChannel();

        // Ensure the order queue exists
        await channel.assertQueue(ORDER_QUEUE, { durable: true });
        // Ensure the billing queue exists
        await channel.assertQueue(BILLING_QUEUE, { durable: true });

        console.log(`Waiting for messages in ${ORDER_QUEUE}. To exit press CTRL+C`);

        // Consume messages from the order queue
        channel.consume(ORDER_QUEUE, async (msg) => {
            if (msg !== null) {
                const orderData = JSON.parse(msg.content.toString());

                // Handle the order processing asynchronously
                handleOrder(orderData).catch(console.error);

                // Acknowledge that the message has been processed
                channel.ack(msg);
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Start consuming orders
consumeOrders();
