from flask import Flask,request
from flask_cors import CORS
import user,project
import json

rootfolder="./global/"
app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
	if request.method == "GET":
		return "API Up and running",200, {"Content-Type":"text/plain"}

@app.route("/coffee")
def coffee():
	return "<h1>*pipes*</h1>", 418,{"Content-Type":"text/html"}

@app.route("/login",methods=["POST"])
def login():
	if request.method == "POST":
		print(request.data.decode("utf-8"))
		data = json.loads(request.data)
		token = user.login(data["name"],data["password"])
		return json.dumps({"name":data["name"],"display-name":"i dont know","auth-token":token}),201,{"Content-Type":"application/json"}
	

@app.route("/logout")
def logout():
	return "",501

@app.route("/projects")
def users():
	
	return str(project.list_projects()),200,{"Content-Type":"text/json"}


