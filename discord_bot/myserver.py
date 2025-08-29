from flask import flask
from threading import Thread

app = flask('')

@app.route('/')
def home():
    return "Server is running!"

def run():
    app.run(host='0.0.0.0',port=8080)

def server_on():
    t = Thread(target=run)
    t.start()