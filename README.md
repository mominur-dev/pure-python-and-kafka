# 📘 Python + Kafka Project Setup (Docker KRaft Mode)

This project demonstrates how to set up Apache Kafka using Docker (without Zookeeper) and connect it with Python producer and consumer applications.

---

# 🚀 1. Project Overview

We will build:

* Kafka broker using Docker Compose (KRaft mode)
* Python Producer (send messages)
* Python Consumer (receive messages)
* Real-time event streaming system

---

# 🧱 2. Kafka Setup (Docker Compose)

We are using Kafka **KRaft mode (no Zookeeper required)**.

## 📄 docker-compose.yaml

```yaml
version: '3.8'

services:
  kafka:
    image: confluentinc/cp-kafka:7.7.8
    container_name: kafka
    ports:
      - "9092:9092"
      - "9093:9093"

    environment:
      # KRaft configuration
      CLUSTER_ID: "mominur_cluster_id_01"
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@kafka:9093"

      # Listener configuration
      KAFKA_LISTENERS: "PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://localhost:9092"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"

      # Internal settings
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1

      # Storage
      KAFKA_LOG_DIRS: "/var/lib/kafka/data"

    volumes:
      - kafka_kraft:/var/lib/kafka/data

volumes:
  kafka_kraft:
```

---

# ▶️ 3. Start Kafka

Run the following command:

```bash
docker-compose up -d
```

Check logs:

```bash
docker logs -f kafka
```

You should see:

```
Kafka Server started
```

---

# 📦 4. Install Python Kafka Client

We use the official Python client:

```bash
pip install confluent-kafka
```

---

# 📤 5. Kafka Producer (Send Data)

Create file: `producer.py`

```python
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(conf)

topic = "test-topic"

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

for i in range(5):
    message = f"Hello Kafka Message {i}"
    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.poll(0)

producer.flush()
```

---

# 📥 6. Kafka Consumer (Receive Data)

Create file: `consumer.py`

```python
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['test-topic'])

print("Listening for messages...")

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print(msg.error())
        continue

    print("Received:", msg.value().decode('utf-8'))
```

---

# ▶️ 7. Run Python Applications

### Step 1: Start Consumer

```bash
python consumer.py
```

### Step 2: Start Producer

```bash
python producer.py
```

---

# 🔁 8. System Architecture

```text
Producer → Kafka Topic → Consumer
```

Flow:

1. Producer sends event
2. Kafka stores event
3. Consumer reads event in real-time

---

# 🧠 9. Key Concepts

| Component  | Description             |
| ---------- | ----------------------- |
| Broker     | Kafka server            |
| Topic      | Message channel         |
| Producer   | Sends data              |
| Consumer   | Reads data              |
| KRaft Mode | Kafka without Zookeeper |
