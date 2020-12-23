from kafka import KafkaProducer
import json
from data import get_registered_user
import time
from server import new_user, view_all

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['192.168.1.8:9092'],
                        value_serializer=json_serializer)

if __name__ == '__main__':
    while True:
        method = input('Do you want to insert or view?\n')

        if method == 'view':
            table = input('Which table would you like to view?\n')
            response = view_all(table)
            producer.send("registered_user", response)
            time.sleep(4)

        if method == 'insert':
            Id_num = input('Enter your ID: ')
            FirstName = input('Enter your First Name: ')
            LastName = input('Enter your Last Name: ')
            Age = input('Enter your Age: ')
            registered_user = new_user(Id_num, FirstName, LastName, Age)
            print(registered_user)
            producer.send("registered_user", registered_user)
            time.sleep(4)
