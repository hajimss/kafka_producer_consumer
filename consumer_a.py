from kafka import KafkaConsumer
from kafka import TopicPartition
import json

if __name__ == '__main__':
    consumer = KafkaConsumer(
        'registered_user',
        bootstrap_servers=['192.168.1.2:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='consumer-group-a'
    )

    print("Connected:", consumer.bootstrap_connected())
    print("Subscription:", consumer.subscription())
    print("starting the consumer...")

    for msg in consumer:
        print("Registered User: {}".format(json.loads(msg.value)))