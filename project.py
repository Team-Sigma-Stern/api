import main
import os

def listprojects(user=""):
    projects = os.listdir(main.rootfolder+"Projects")
    for project in projects:
        if user == "" and 
