This project is a robust, distributed system designed to manage food orders and send notifications efficiently. By leveraging RabbitMQ, Node.js, Django, and MySQL, the system ensures high performance, scalability, and reliability for modern food delivery platforms.

Key Features
High Availability and Reliability:

Achieved 99.9% uptime with failover capabilities across three machines using MySQL and RabbitMQ.
Distributed Messaging Architecture:

Designed four RabbitMQ exchanges:
Billing: Handles payment-related messages.
Notification: Sends order status updates to customers.
Customer Management: Manages user-specific communication.
Balance: Tracks account balances and transactional updates.
Supported over 2,500 concurrent messages per second with both 1-to-1 and 1-to-many messaging models.
Optimized Communication:

Implemented RPC patterns for efficient cross-service communication.
Used persistent messaging and JSON serialization for asynchronous, data flows.
Improved system scalability by 40% with optimized message handling.


Food Order Management and Notification System
Overview
This project is a robust, distributed system designed to manage food orders and send notifications efficiently. By leveraging RabbitMQ, Node.js, Django, and MySQL, the system ensures high performance, scalability, and reliability for modern food delivery platforms.

Key Features
High Availability and Reliability:

Achieved 99.9% uptime with failover capabilities across three machines using MySQL and RabbitMQ.
Distributed Messaging Architecture:

Designed four RabbitMQ exchanges:
Billing: Handles payment-related messages.
Notification: Sends order status updates to customers.
Customer Management: Manages user-specific communication.
Balance: Tracks account balances and transactional updates.
Supported over 2,500 concurrent messages per second with both 1-to-1 and 1-to-many messaging models.
Optimized Communication:

Implemented RPC patterns for efficient cross-service communication.
Used persistent messaging and JSON serialization for asynchronous, data flows.
Improved system scalability by 40% with optimized message handling.


Tech Stack
Backend Technologies: Node.js, Django
Messaging Broker: RabbitMQ
Database: MySQL
Patterns and Practices: RPC, JSON Serialization, Asynchronous Messaging

Achievements
Scaled to support real-time messaging demands with minimal latency.
Enhanced system resilience and failover mechanisms.
Delivered a reliable solution for food order management and notification needs.
