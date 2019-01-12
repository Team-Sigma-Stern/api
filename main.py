from flask import Flask,request
import user,project
import json

rootfolder="./global/"
app = Flask(__name__)

@app.route("/")
def Hello():
    return "Hello here is the api"

@app.route("/user")
def users():
	response="couldn't process your request ;("
	response=user.get_user_list()
	return response

