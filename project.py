from pathlib import Path
import os
import json
import main

def list_projects(user="any",role="any"):
    projects = os.listdir(main.rootfolder+"Projects")
    for project in projects:
        if not (user == "any" or has_role(project,user,role)):
            # or not Path(main.rootfolder+"Projects/"+project+"/project.json").is_file():
            projects.remove(project)
    return projects
# hasrole
# checks if a given user has the given role
# returns False if the user isnt a member,
# True if the user has the given role and
# the role if the user is a member and the given role is any
def has_role(project,user,role="any"):
    with open(main.rootfolder+"Projects/"+project+"/project.json") as project_file:
        project_file = json.load(project_file)
        members = project_file["members"]
        for member in members:
            if member["name"] == user:
                if role == "any":
                    return member["role"]
                if member["role"] == role:
                    return True
    return False

def list_files(project):
    files = os.listdir(main.rootfolder+"Projects/"+project)
    for file in files:
        if file == "project.json":
            files.remove(file)
    return files

def lock(project,file,user):
    if(not Path(main.rootfolder+"Projects/"+project+"/"+file).is_file()):
        return "Error: File dont Exists"
    with open(main.rootfolder+"Projects/"+project+"/project.json") as project_file:
        project_conf = json.load(project_file)
        if(check_locked(project,file)):
            if check_locked(project,file,user):
                return "Success: File Allreadylocked"
            else:
                return "Error: file Allready Locked"
        project_conf["locks"].append({"file":file,"user":user})
    
    with open(main.rootfolder+"Projects/"+project+"/project.json","w") as project_file:
        json.dump(project_conf,project_file,indent=4)
    return "Success: Locked"


def check_locked(project,file,user="any"):
    with open(main.rootfolder+"Projects/"+project+"/project.json") as project_file:
        project_file = json.load(project_file)
        for lock in project_file["locks"]:
            if lock["file"] == file and (user == "any" or  lock["user"] == user):
                return True
        return False

def unlock(project,file,user): 
    if(not check_locked(project,file)):
            return "Success: file not Locked"
    if(not check_locked(project,file,user)):
        return "Error: File not Locked by "+user
    with open(main.rootfolder+"Projects/"+project+"/project.json") as project_file:
        project_conf = json.load(project_file)
       
        if(check_locked(project,file,user)):
            project_conf["locks"].remove({"file":file,"user":user})

    with open(main.rootfolder+"Projects/"+project+"/project.json","w") as project_file:
        json.dump(project_conf,project_file,indent=4)
    return "Success: Unlocked"

def setFile(project,file,user,content):
    pass

def getFile(project,file,user):
    pass

def addFile(project,file,user):
    pass

def removeFile(project,file,user):
    pass

def renameFile(project,file,user,new_file_name):
    pass