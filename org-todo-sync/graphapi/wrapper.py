import datetime
from auth import get_oauth_session
import json


BASE_URL = "https://graph.microsoft.com/v1.0/me/todo/lists"

def parse_response(response):
    return json.loads(response.content.decode())["value"]

def get_tasks(list_id):
    session = get_oauth_session()
    endpoint=f"{BASE_URL}/{list_id}/tasks"
    response = session.get(endpoint)
    response_value = parse_response(response)
    return response_value

def get_lists():
    session = get_oauth_session()
    endpoint=f"{BASE_URL}"
    response = session.get(endpoint)
    response_value = parse_response(response)
    return response_value

def create_list():
    return None


def create_task(org_todo, list_id):
    endpoint = f"{BASE_URL}/{list_id}/tasks"
    request_body = {
        "title": '{keyword} {heading}'.format(keyword=org_todo.todo, heading=org_todo.heading),
        "isReminderOn": org_todo.remind,
}
    if org_todo.scheduled:
        request_body["reminderDateTime"] = org_todo.scheduled
    if org_todo.deadline:
        request_body["dueDateTime"] = org_todo.deadline
    elif org_todo.scheduled:
        request_body["dueDateTime"] = org_todo.scheduled
    if org_todo.repeat:
        request_body["recurrence"] = org_todo.repeat
    if org_todo.body:
        request_body["body"] = { "content":org_todo.body, "contentType":"text" }
    if org_todo.closed:
        request_body["completedDateTime"] = org_todo.closed
        request_body["status"] = "completed"
    session = get_oauth_session()
    response = session.post(endpoint, json=request_body)
    return True if response.ok else response.raise_for_status()
