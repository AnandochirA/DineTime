import amqp from 'amqplib';

async function startConsumers() {
    try {
        const connection = await amqp.connect('amqp://anand:2004anand@10.204.4.76');
        const channel = await connection.createChannel();

        const SYSTEM_QUEUE = 'system-queue';
        const SMS_QUEUE = 'SMS-queue';
        const EMAIL_QUEUE = 'email-queue';

        await channel.assertQueue(SYSTEM_QUEUE, { durable: true });
        await channel.assertQueue(SMS_QUEUE, { durable: true });
        await channel.assertQueue(EMAIL_QUEUE, { durable: true });

        console.log(`Waiting for messages in ${SYSTEM_QUEUE}, ${SMS_QUEUE}, and ${EMAIL_QUEUE}...`);

        channel.consume(SYSTEM_QUEUE, (msg) => {
            if (msg !== null) {
                const messageContent = msg.content.toString();
                console.log(`Received message from system queue: ${messageContent}`);
                channel.ack(msg);
            }
        });

        channel.consume(SMS_QUEUE, (msg) => {
            if (msg !== null) {
                const messageContent = msg.content.toString();
                console.log(`Received message from SMS queue: ${messageContent}`);
                channel.ack(msg);
            }
        });

        channel.consume(EMAIL_QUEUE, (msg) => {
            if (msg !== null) {
                const messageContent = msg.content.toString();
                console.log(`Received message from email queue: ${messageContent}`);
                channel.ack(msg);
            }
        });

    } catch (error) {
        console.error('Error in consumer setup:', error);
    }
}

startConsumers();
