import { connect } from 'amqplib';

const ORDER_QUEUE = 'order-queue';
const BILLING_QUEUE = 'billing-queue';
const BILLING_EXCHANGE = 'billing_exchange';
const BILLING_ROUTING_KEY = 'billing_routing_key';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function handleOrder(orderData, channel) {
    console.log("Received order:", orderData);
    try {
        if (orderData.event == "order_created") {
            const waitTime = orderData.minutesToTake * 60 * 1000; 
            await delay(waitTime);
            console.log(`Waited ${orderData.minutesToTake} minutes for order ${orderData.order_id}.`);

            const billingData = {
                event: "order_created",
                order_id: orderData.order_id,
                customer_id: orderData.customer_id,
                total_amount: orderData.total_amount,
            };

            channel.publish(BILLING_EXCHANGE, BILLING_ROUTING_KEY, Buffer.from(JSON.stringify(billingData)), { persistent: true });
            console.log("Sent billing data to billing-queue:", billingData);

        }
        else if (orderData.event == "order_updated") {
            const waitTime = orderData.minutesToTake * 60 * 1000;
            await delay(waitTime);
            console.log(`Waited UpdatedOrder ${orderData.minutesToTake} minutes for order ${orderData.order_id}.`);

            const billingData = {
                event: "order_updated",
                order_id: orderData.order_id,
                customer_id: orderData.customer_id,
                refund: orderData.refund,
                extraPayment: orderData.extraPayment,
            };

            channel.publish(BILLING_EXCHANGE, BILLING_ROUTING_KEY, Buffer.from(JSON.stringify(billingData)), { persistent: true });
            console.log("Sent billing data to billing-queue:", billingData);
        }
    } catch (error) {
        console.error('Error:', error)
    }
}

async function consumeOrders() {
    try {
        const connection = await connect('amqp://anand:2004anand@10.204.4.76');
        const channel = await connection.createChannel();

        await channel.assertQueue(ORDER_QUEUE, { durable: true });
        console.log(`Queue "${ORDER_QUEUE}" is ready.`);

        await channel.assertQueue(BILLING_QUEUE, { durable: true });
        console.log(`Queue "${BILLING_QUEUE}" is ready.`);

        console.log(`Waiting for messages in ${ORDER_QUEUE}. To exit press CTRL+C`);

        channel.consume(ORDER_QUEUE, async (msg) => {
            if (msg !== null) {
                const orderData = JSON.parse(msg.content.toString()); 
                
                await handleOrder(orderData, channel);
                channel.ack(msg); 
                console.log(`Acknowledged message: ${msg.content.toString()}`);
            } else {
                console.log('Received null message, skipping.');
            }
        }, { noAck: false });

    } catch (error) {
        console.error('Error:', error);
    }
}
consumeOrders();
