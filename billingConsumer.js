import { connect } from 'amqplib';

const BILLING_QUEUE = 'billing-queue';

async function handleOrder(billingData) {
    console.log("Received order:", billingData);

    if (orderData.status === 'completed') {
        
        channel.sendToQueue(BILLING_QUEUE, Buffer.from(JSON.stringify(billingData)), { persistent: true });
        console.log("Sent billing data to billing-queue:", billingData);
    }
}

async function consumeOrders() {
    try {
        // Connect to RabbitMQ
        const connection = await connect('amqp://your-rpi-ip-address');
        const channel = await connection.createChannel();

        await channel.assertQueue(ORDER_QUEUE, { durable: true });
        await channel.assertQueue(BILLING_QUEUE, { durable: true });

        console.log(`Waiting for messages in ${ORDER_QUEUE}. To exit press CTRL+C`);

        channel.consume(ORDER_QUEUE, async (msg) => {
            if (msg !== null) {
                const orderData = JSON.parse(msg.content.toString());

                handleOrder(orderData).catch(console.error);

                channel.ack(msg);
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

consumeOrders();
