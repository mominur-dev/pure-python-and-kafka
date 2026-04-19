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

for i in range(10):
    message = f"Hello Kafka Message {i}"
    producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
    producer.poll(0)

producer.flush()