from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "$Response"

@app.route("/sub")
def sub():
    return "$Other_Response"