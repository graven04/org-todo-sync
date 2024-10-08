import time
import datetime
import graphapi.graphapi as api
import json


BASE_URL = "https://graph.microsoft.com/v1.0/me/todo/lists"


def parse_response(response):
    return json.loads(response.content.decode())["value"]


def get_tasks(list_id):
    session = api.get_oauth_session()
    endpoint = f"{BASE_URL}/{list_id}/tasks"
    response = session.get(endpoint)
    response_value = parse_response(response)
    return response_value


def get_list(name):
    session = api.get_oauth_session()
    endpoint = f"https://graph.microsoft.com/v1.0/me/todo/lists?$filter=displayName eq '{name}'"
    response = session.get(endpoint)
    response_value = parse_response(response)
    print(response_value)
    dictionary = response_value[0]
    list_id = dictionary['id']
    return list_id


def get_lists():
    session = api.get_oauth_session()
    endpoint = "https://graph.microsoft.com/v1.0/me/todo/lists"
    response = session.get(endpoint)
    response_value = parse_response(response)
    list_ids = [x['id'] for x in response_value
                if x.get('wellknownListName') == 'none']
    return list_ids


def create_list(name):
    ''' create a ms todo list with the name of input and output the id of
    the list created'''
    endpoint = BASE_URL
    request_body = {"displayName": "{list_name}".format(list_name=name)}
    session = api.get_oauth_session()
    response = session.post(endpoint, json=request_body)
    list_id = json.loads(response.content.decode())["id"]
    return list_id if response.ok else response.raise_for_status()


def delete_list(list_id):
    ''' delete a ms todo list with the id of input and output True if successful'''
    endpoint = f"{BASE_URL}/{list_id}"
    session = api.get_oauth_session()
    response = session.delete(endpoint)
    return True if response.ok else response.raise_for_status()


def purge_lists(list_ids):
    ''' takes a list of todo list ids and deletes the list'''
    for i in list_ids:
        delete_list(i)


def create_task(org_todo, list_id):
    endpoint = f"{BASE_URL}/{list_id}/tasks"
    request_body = {
        "title": '{keyword} {heading}'.format(keyword=org_todo.todo,
                                              heading=org_todo.heading),
        "isReminderOn": org_todo.remind}
    if org_todo.scheduled:
        request_body["reminderDateTime"] = org_todo.scheduled
        request_body["startDateTime"] = org_todo.scheduled
    if org_todo.deadline:
        request_body["dueDateTime"] = org_todo.deadline
    if org_todo.repeat:
        request_body["recurrence"] = org_todo.repeat
    if org_todo.body:
        request_body["body"] = {"content": org_todo.body, "contentType": "text"}
    if org_todo.closed:
        request_body["completedDateTime"] = org_todo.closed
        request_body["status"] = "completed"
    session = api.get_oauth_session()
    response = session.post(endpoint, json=request_body)
    return True if response.ok else response.raise_for_status()


def create_project_list():
    endpoint = f"{BASE_URL}"
    request_body = {"displayName": "Projects"}
    session = api.get_oauth_session()
    response = session.post(endpoint, json=request_body)
    list_id = json.loads(response.content.decode())["id"]
    return list_id if response.ok else response.raise_for_status()


def create_project_task(project_head, project_children, list_id):
    endpoint = f"{BASE_URL}/{list_id}/tasks"
    project = "{keyword} {heading}".format(keyword=project_head.todo, heading=project_head.heading)
    request_body = {
        "title": '{project} || {keyword} {heading}'.format(project=project, keyword=project_children.todo, heading=project_children.heading),
        "isReminderOn": project_children.remind, }
    if project_children.scheduled:
        request_body["reminderDateTime"] = project_children.scheduled
        request_body["startDateTime"] = project_children.scheduled
    if project_children.deadline:
        request_body["dueDateTime"] = project_children.deadline
    if project_children.repeat:
        request_body["recurrence"] = project_children.repeat
    if project_children.body:
        request_body["body"] = {"content": project_children.body, "contentType": "text"}
    if project_children.closed:
        request_body["completedDateTime"] = project_children.closed
        request_body["status"] = "completed"
    session = api.get_oauth_session()
    response = session.post(endpoint, json=request_body)
    return True if response.ok else response.raise_for_status()
