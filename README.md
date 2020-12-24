# kafka_producer_consumer
An application that showcases the interaction of producers and consumers with Kafka

To implement kafka, run zookeper and kafka to ave a kafka server running. Then run consumer.py locally. This will consume the messages that is published by the producer application.

__Stack__
Web Framework: Flask
Database: MySQL

__Steps__
1. Run zookeeper application in the kafka_2.13-2.6.0 folder
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```
2. Run Kafka server in the same folder
```
JMX_PORT=8004 bin/kafka-server-start.sh config/server.properties 
```
3. Run Kafka Manager and create the topics in the cmak-3.0.0.5 folder
```
bin/cmak -Dconfig.file=conf/application.conf -Dhttp.port8080
```
4. Use the flask app to do tasks that is done by producers
```
python producers.py
```
5. Run consumer.py to consume the messages
```
python consumers.py
```