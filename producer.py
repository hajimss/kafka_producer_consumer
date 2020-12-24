from flask import Flask, request, redirect, render_template, url_for, session
from kafka import KafkaProducer
import json
from data import get_registered_user
import time
from server import new_user, view_all, delete_user

app = Flask(__name__)

app.secret_key = "secret"

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer1 = KafkaProducer(bootstrap_servers=['192.168.1.8:9092'],
                        value_serializer=json_serializer)

producer2 = KafkaProducer(bootstrap_servers=['192.168.1.8:9092'],
                        value_serializer=json_serializer)

producer3 = KafkaProducer(bootstrap_servers=['192.168.1.8:9092'],
                        value_serializer=json_serializer)

producer_dict = { 
    "producer1": [producer1, "Producer 1"], 
    "producer2": [producer2, "Producer 2"], 
    "producer3": [producer3, "Producer 3"]
    }
##############################################################################################

@app.route('/')
def home():
    if "producer" in session:
        return redirect(url_for("user"))
    return redirect(url_for("login"))

##############################################################################################

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "producer" not in session:
        print("None in session")
    if request.method == 'POST':
        session["producer"] = request.form['producer']
        return redirect(url_for('user'))
    return render_template("login.html")

##############################################################################################

@app.route('/logout')
def logout():
    session.pop("producer", None)
    return redirect(url_for("login"))

##############################################################################################

@app.route('/user', methods=['GET','POST'])
def user():
    if "producer" not in session:
        return redirect(url_for("login"))
    else:
        print(session["producer"])
        return render_template("user.html", producer=producer_dict[session["producer"]][1])

##############################################################################################

@app.route('/viewtable')
def viewtable():
    if "producer" in session:
        response = view_all('Persons')
        producer_dict[session["producer"]][0].send("registered_user", "{} viewed Persons.".format(producer_dict[session["producer"]][1]))
        print(session["producer"])
        return render_template("viewtable.html", response=response)
    else: redirect(url_for("login"))


##############################################################################################

@app.route('/newuser', methods=["GET", "POST"])
def newuser():
    if request.method == "POST":
        registered_user = new_user(request.form['id'], request.form['fname'], request.form['lname'], request.form['age'])
        print(registered_user)
        producer_dict[session["producer"]][0].send("registered_user", registered_user + " by {}".format(producer_dict[session["producer"]][1]))
        return redirect(url_for("user"))
    else:
        return render_template("newuser.html")

##############################################################################################

@app.route('/deleteuser/<id>', methods=["GET"])
def deleteuser(id):
    if "producer" not in session:
        return redirect(url_for("login"))
    if request.method == 'GET':
        response = delete_user(id)
        producer_dict[session["producer"]][0].send("registered_user", response + " by {}".format(producer_dict[session["producer"]][1]))
        return redirect(url_for("user"))

##############################################################################################

if __name__ == '__main__':
    app.run(port=5000, debug=True)
