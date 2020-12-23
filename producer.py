from flask import Flask, request, redirect, render_template, url_for
from kafka import KafkaProducer
import json
from data import get_registered_user
import time
from server import new_user, view_all

app = Flask(__name__)

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(bootstrap_servers=['192.168.1.8:9092'],
                        value_serializer=json_serializer)

##############################################################################################

@app.route('/user', methods=['GET','POST'])
def user():
    if request.method == 'GET':
        return render_template("user.html")

    if request.method =='POST':
        Id_num = input('Enter your ID: ')
        FirstName = input('Enter your First Name: ')
        LastName = input('Enter your Last Name: ')
        Age = input('Enter your Age: ')
        registered_user = new_user(Id_num, FirstName, LastName, Age)
        print(registered_user)
        producer.send("registered_user", registered_user)
        time.sleep(4)
        return render_template("user.html")

##############################################################################################

@app.route('/viewtable')
def viewtable():
    response = view_all('Persons')
    producer.send("registered_user", "Someone viewed Persons.")
    return render_template("viewtable.html", response=response)


##############################################################################################

if __name__ == '__main__':
    app.run(port=5000, debug=True)
