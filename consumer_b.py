from kafka import KafkaConsumer
from kafka import TopicPartition
import json

if __name__ == '__main__':
    consumer = KafkaConsumer(
        'registered_user',
        bootstrap_servers=['192.168.1.2:9092'],
        auto_offset_reset='earliest',
        group_id='consumer-group-b'
    )

    print("starting the consumer...")

    for msg in consumer:
        print("Registered User: {}".format(json.loads(msg.value)))