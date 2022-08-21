import json
from time import sleep
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

import requests

import structures



def requestJSON(token: str, url) -> Optional[str]:
    """
    Send a request using the (access) token + url and get a json response back.

    parameters:
        token: The access token
        url:   The api endpoint to get the json from

    returns: Either the content in json format, or None if nothing was found
    """
    if (message := requests.get(url + f"?access_token={token}")).status_code == 200:
        return message.json()
    return None

def getOrSaveUser() -> structures.User:
    """
    Either gets the accesstoken and domain from 'accesstoken.txt',
    or asks the user for the token + domain and creates the aforementioned file.
    
    returns: The access token and domain
    """
    tokenpath = Path("accesstoken.txt")
    if not Path.exists(tokenpath):
        token = input("Please provide your access token: ")
        domain = input("Please provide the domain of your canvas: ").replace("/","").strip()
        with open(tokenpath, "w+") as file:
            file.write(f"{token}\n{domain}")
    else:
        with open(tokenpath, "r") as file:
            token, domain = file.readlines()
            
    return structures.User(token, domain)

def getCourseIds(token: str) -> list[int]:
    """
    Gets a list of current course ids for the current user.

    parameters:
        token: The access token

    returns: A list of current course ids
    """
    coursesurl = f"https://canvas.instructure.com/api/v1/courses"
    jsoncourses = requestJSON(token, coursesurl)
    if jsoncourses is None:
        jsoncourses = []
    formatIsoDate: Callable[[str], datetime] = \
     lambda date: datetime.fromordinal(0) if date is None else datetime.fromisoformat(date[:-1])
    ids = [course["id"] for course in jsoncourses if formatIsoDate(course["end_at"]) > datetime.now()]
    return ids

def getUserId(token: str) -> int:
    """
    Gets the current user id

    parameters:
        token: The access token

    returns: The current user id
    """
    coursesurl = f"https://canvas.instructure.com/api/v1/courses"
    jsoncourses = requestJSON(token, coursesurl)
    return jsoncourses[0]["enrollments"][0]["user_id"]


def upcomingAssignments(token: str, *courseIds : int) -> list[structures.Assignment]:
    """
    Gets a list of structures.Assignments based on the upcoming assignments.

    parameters:
        token: The access token
        courseIds: One or more course ids

    returns: A list of structures.Assignments based on the upcoming assignments
    """
    assignmentList = []
    for courseId in courseIds:

        assignmentUrl = f"https://canvas.instructure.com/api/v1/courses/{courseId}/assignments"
        assignmentJson = requestJSON(token, assignmentUrl)

        if assignmentJson is None: continue
        for assignment in assignmentJson:

            # If assignment is locked
            if lock := assignment.get("lock_at"):
                if datetime.fromisoformat(lock[:-1]) < datetime.now(): continue

            # Get due date if exists
            if due := assignment.get("due_at"): 
                due_date = datetime.fromisoformat(due[:-1]) 
            else: 
                due_date = None

            # Append assignments 
            assignmentList.append(structures.Assignment(
                assignment["id"], 
                assignment["name"], 
                due_date,
                )
            )
        sleep(.25)
    return assignmentList

def todoItems(token: str):
    """
    Gets a list of todo items for the current user

    parameters:
        token: The access token

    returns: A List of todos for the current user
    """
    url = f"https://canvas.instructure.com/api/v1/users/self/todo"
    todoJson = requestJSON(token, url)
    print(todoJson)
    print(json.dumps(todoJson, indent=4, sort_keys=True))

def upcomingEvents(token: str):
    """
    Gets a list of upcoming events for the current user

    parameters:
        token: The access token

    returns: A List of events for the current user
    """
    url = f"https://canvas.instructure.com/api/v1/users/self/upcoming_events"
    upcomingJson = requestJSON(token, url)
    print(json.dumps(upcomingJson, indent=4, sort_keys=True))

    
    



if __name__ == "__main__":
    user = structures.User('2087~xDVs23GQKea17nmzGlEAb9yC19izhXYQieUGInQgHeIZ8bXdbneHLrz5ubAsfu3i', 'iechs.instructure.org')
    #userid = getUserId(token)
    upcomingAssignments(user.utoken)
