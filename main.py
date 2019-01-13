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

@app.route("/projects/<project_name>/files",methods=["GET"])
def project_files(project_name):
	user = get_user(request)
	if user == None:
		return error_response("No token provided or token expired",401)
	if not project.has_role(project_name,user):
		return error_response("You dont have access here",404)

	if project_name not in project.list_projects():
		return error_response("project not found or no Access",404)
	return json.dumps(project.list_files(project_name)),200,{"Content-Type":"application/json"}

@app.route("/projects/<project_name>/files/<file_name>",methods=["POST","GET"])
def file(project_name,file_name):
	user = get_user(request)
	if not project.has_role(project_name,user):
		return error_response("You dont have access here",404)
	if user == None:
		return error_response("You need to be logged in",401)
	if request.method == "GET":
		return project.get_file(project_name,file_name,user), 200, {"Content-Type":"plain/text"}
	if request.method == "POST":
		if project.has_role(project_name,user,"guest"):
			return error_response("You are not allowed to write",400)
		if not project.check_locked(project_name,file_name,user):
			if project.check_locked(project_name,file_name):
				return error_response("The File is locked by someone else",403)
			else:
				return error_response("You need to lock the file first",403)
		project.setFile(project_name,file_name,user,request.data)

@app.route("/projects/<project_name>/files/<file_name>/lock",methods=["POST","GET"])
def lock(project_name,file_name):
	user = get_user(request)
	if not project.has_role(project_name,user):
		return error_response("You dont have access here",404)
	if user == None:
		return error_response("You need to be logged in",401)
	if request.method == "GET":
		response_val = "No"
		if project.check_locked(project_name,file_name):
			response_val = "Other"
			if project.check_locked(project_name,file_name,user):
				response_val = "Yes"
		return json.dumps({"locked":response_val}),200,{"Content-Type":"application/json"}
	if request.method == "POST":
		if "Success" in project.lock(project_name,file_name,user):
			return "",201
		else:
			return error_response("File allready locked",400)

@app.route("/projects/<project_name>/files/<file_name>/unlock",methods=["POST"])
def unlock(project_name,file_name):
	user = get_user(request)
	if not project.has_role(project_name,user):
		return error_response("You dont have access here",404)
	if user == None:
		return error_response("You need to be logged in",401)
	if project.check_locked(project_name,file_name,user):
		project.unlock(project_name,file_name,user)
		return "",2001
	else:
		return error_response("File Locked by other User",400)

def get_user(request):
	authtoken = json.loads(request.headers.get("auth-token"))
	if user.authenticated(authtoken):
		return authtoken["user"]

def error_response(message,code):
	return json.dumps({"message":message}),code,{"Content-Type":"application/json"}


