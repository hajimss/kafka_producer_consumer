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
    return render_template("user.html")

##############################################################################################

@app.route('/viewtable')
def viewtable():
    response = view_all('Persons')
    producer.send("registered_user", "Someone viewed Persons.")
    return render_template("viewtable.html", response=response)


##############################################################################################

@app.route('/newuser', methods=["GET", "POST"])
def newuser():
    if request.method == "POST":
        registered_user = new_user(request.form['id'], request.form['fname'], request.form['lname'], request.form['age'])
        print(registered_user)
        producer.send("registered_user", registered_user)
        return redirect(url_for("user"))
    else:
        return render_template("newuser.html")

##############################################################################################

if __name__ == '__main__':
    app.run(port=5000, debug=True)
