import json
from time import sleep
from datetime import datetime
from pathlib import Path

import requests


def requestJSON(token: str, url):
    return requests.get(url + f"?access_token={token}").json()
def getOrCreateFile():
    tokenpath = Path("accesstoken.txt")
    if not Path.exists(tokenpath):
        token = input("Please provide your access token: ")
        with open(tokenpath, "w+") as file:
            file.write(token)
    else:
        with open(tokenpath, "r") as file:
            token = file.read()
    return token
def getCourseIds(token: str) -> list[int]:
    coursesurl = f"https://canvas.instructure.com/api/v1/courses"
    jsoncourses = requestJSON(token, coursesurl)

    ids = []
    for course in jsoncourses:
        if datetime.fromisoformat(course["end_at"][:-1]) > datetime.now():
            ids.append(course["id"])
    return ids
def getUserId(token: str):
    coursesurl = f"https://canvas.instructure.com/api/v1/courses"
    jsoncourses = requestJSON(token, coursesurl)
    return jsoncourses[0]["enrollments"][0]["user_id"]

def getAssignmentsFromCourseId(token: str, *courseIds : int):
    for courseId in courseIds:
        assignmentUrl = f"https://canvas.instructure.com/api/v1/courses/{courseId}/assignments"
        assignmentJson = requestJSON(token, assignmentUrl)
        print(json.dumps(assignmentJson, indent=4, sort_keys=True))

def todoItems(token: str):
    url = f"https://canvas.instructure.com/api/v1/users/self/todo"
    todoJson = requestJSON(token, url)
    print(json.dumps(todoJson, indent=4, sort_keys=True))

def upcomingEvents(token: str):
    url = f"https://canvas.instructure.com/api/v1/users/self/upcoming_events"
    upcomingJson = requestJSON(token, url)
    
    



if __name__ == "__main__":
    token = getOrCreateFile()
    userid = getUserId(token)
    #getAssignmentsFromCourseId(token, getCourseIds(token)[0])
    todoItems(token)

# due_at
# allowed_attempts
# html_url
# name