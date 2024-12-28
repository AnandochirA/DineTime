import { connect } from 'amqplib';

async function startConsumer() {
    try {
        const connection = await connect('amqp://anand:2004anand@10.204.4.76');
        const channel = await connection.createChannel();

        const NOTIFICATION_QUEUE = 'notification-queue';
        await channel.assertQueue(NOTIFICATION_QUEUE, { durable: true });

        const SYSTEM_EXCHANGE = 'system_exchange';
        const SMS_EXCHANGE = 'SMS_exchange';
        const EMAIL_EXCHANGE = 'email_exchange';

        const SYSTEM_QUEUE = 'system-queue';
        const SMS_QUEUE = 'SMS-queue';
        const EMAIL_QUEUE = 'email-queue';

        await channel.assertQueue(SYSTEM_QUEUE, { durable: true });
        await channel.assertQueue(SMS_QUEUE, { durable: true });
        await channel.assertQueue(EMAIL_QUEUE, { durable: true });

        await channel.bindQueue(SYSTEM_QUEUE, SYSTEM_EXCHANGE, 'system');
        await channel.bindQueue(SMS_QUEUE, SMS_EXCHANGE, 'sms');
        await channel.bindQueue(EMAIL_QUEUE, EMAIL_EXCHANGE, 'email');

        console.log(`Waiting for messages in ${NOTIFICATION_QUEUE}...`);

        channel.consume(NOTIFICATION_QUEUE, (msg) => {
            if (msg !== null) {
                const messageContent = msg.content.toString();
                console.log(`Received message: ${messageContent}`);

                const { customer_id: customerId, order_id: orderId, message } = JSON.parse(messageContent);
                
                let systemMessage, smsMessage, emailMessage;
                systemMessage = {
                    status: 'Success',
                    notif: `Customer Number ${customerId}, your order ${orderId} is ready to pick up. Payment is completed successfully. More info: ${message}`
                };
                smsMessage = {
                    status: 'Success',
                    notif: `Customer ${customerId}, your order ${orderId} is ready for pickup. Payment completed successfully.`
                };
                emailMessage = {
                    status: 'Success',
                    notif: `Dear Customer ${customerId}, your order ${orderId} is ready for pickup. Payment has been completed successfully. More info: ${message}`
                };

                // Publish to each specific exchange
                channel.publish(SYSTEM_EXCHANGE, 'system', Buffer.from(JSON.stringify(systemMessage)), { persistent: true });
                console.log('Sent Notification to system queue');

                channel.publish(SMS_EXCHANGE, 'sms', Buffer.from(JSON.stringify(smsMessage)), { persistent: true });
                console.log('Sent Notification to SMS queue');

                channel.publish(EMAIL_EXCHANGE, 'email', Buffer.from(JSON.stringify(emailMessage)), { persistent: true });
                console.log('Sent Notification to email queue');

                channel.ack(msg);
            }
        });
    } catch (error) {
        console.error('Error in consumer setup:', error);
    }
}

startConsumer();
