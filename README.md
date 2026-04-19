This project demonstrates how to set up Apache Kafka using Docker (without Zookeeper) and connect it with Python producer and consumer applications.

---

# Project Overview

We will build:

* Kafka broker using Docker Compose (KRaft mode)
* Python Producer (send messages)
* Python Consumer (receive messages)
* Real-time event streaming system

---

# Kafka Setup (Docker Compose)

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

# Start Kafka

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

# Install Python Kafka Client

We use the official Python client:

```bash
pip install confluent-kafka
```


---

# Run Python Applications

### Step 1: Start Consumer in three diffrent tabs

```bash
python consumer_payments.py
python consumer_rides.py
python consumer_tracking.py

```

### Step 2: Start Producer

```bash
python producer.py
```
