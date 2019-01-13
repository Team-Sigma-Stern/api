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
	print(request.data.decode("utf-8"))
	data = json.loads(request.data)
	token = user.login(data["name"],data["password"])
	if token != None:
		return json.dumps({"name":data["name"],"display-name":"i dont know","auth-token":token}),201,{"Content-Type":"application/json"}
	else:
		return json.dumps({"message":"Wrong username or Password!"}),400,{"Content-Type":"application/json"}

@app.route("/logout",methods=["POST"])
def logout():
	authtoken = json.loads(request.headers.get("auth-token"))
	if user.authenticated(authtoken):
		user.logout(authtoken)
		return "",201
	else:
		return error_response("Invalid auth_token",401)

@app.route("/projects")
def projects():
	
	return str(project.list_projects()),200,{"Content-Type":"application/json"}

@app.route("/projects/<project_name>",methods=["GET"])
def project_files(project_name):
	#user = get_user(request)
	if project_name not in project.list_projects():
		return error_response("project not found or no Access",404)
	return json.dumps(project.list_files(project_name)),200,{"Content-Type":"application/json"}


def get_user(request):
	authtoken = json.loads(request.headers.get("auth-token"))
	if user.authenticated(authtoken):
		return authtoken["user"]

def error_response(message,code):
	return json.dumps({"message":message}),code,{"Content-Type":"application/json"}


