import main
import json
import datetime
auth_tokens=[]

def get_user_list(secure=True):
    users=json.load(open(main.rootfolder+"users.json",encoding="utf-8"))["users"]
    if secure:
        for user in users:
            user.pop("password")
    return str(users)

def create_user(name,displayname="",password=""):
    with open(main.rootfolder+"users.json","r",encoding="utf-8") as user_file:
        users=json.load(user_file)
        print(str(users))
        for user in users["users"]:
            if user["name"] == name:
                return "Failed:User Allready Exists"
        
        new_user = {
            "name": name,
            "displayname": displayname,
            "password":password
        }
        users["users"].append(new_user)
        print(str(users))
    
    with open(main.rootfolder+"users.json","w",encoding="utf-8") as user_file:
        
        json.dump(users,user_file,indent=4,sort_keys=True)
        return "Success: User "+ displayname +" created"

def login(user,password):
    new_token = {"user":user,"expires": (datetime.datetime.utcnow()+datetime.timedelta(minutes=5)).timestamp()}
    auth_tokens.append(new_token)
    return new_token

def logout(auth_token):
    for token in auth_tokens:
        if token["user"]==auth_token["user"]:
            auth_tokens.remove(auth_token)


def authenticated(auth_token):
    remove_invalid_tokens()
    for token in auth_tokens:
        print(token)
        if(token["user"]==auth_token["user"]):
            return True
    return False

def remove_invalid_tokens():
    for token in auth_tokens:
        if datetime.datetime.fromtimestamp(token["expires"]) <= datetime.datetime.utcnow():
            logout(token)
        



