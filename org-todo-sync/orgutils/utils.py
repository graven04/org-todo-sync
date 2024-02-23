from orgparse import load, loads
from orgparse import OrgEnv
import os
import yaml # pip install pyyaml
import datetime


############################################################
#                   org files config section               #
############################################################

def make_config():
    '''make a config direectory if it doesn't exist already'''
    config_dir = "{}/.config/org-todo-sync".format(os.path.expanduser("~"))
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    return config_dir

config_dir = make_config()

def make_folder_config_and_return_folder_path():
    ''' make files config path if it doesnt alrready exist and return instructions or org folder path'''
    files_config_path = os.path.join(config_dir, "files.yml")
    
    # try to load files and list file paths
    if not os.path.isfile(files_config_path):
        files_config_content = {"folder_path": "replace me"}
        
        with open(files_config_path, "w") as f:
            yaml.dump(files_config_content, f)
        print("please edit files.yml in {} in format described here:\n{}".format(config_dir,
                "https://github.com/graven04/org-todo-sync/blob/main/README.org"))
        exit()
    else:
        # Load file paths
        with open(files_config_path) as f:
            files_config_content = yaml.load(f, yaml.SafeLoader)
        if (not os.path.isdir(files_config_content["folder_path"])) or files_config_content["folder_path"] == "replace_me":
            print("Either folder does not exist or folder path has not been added to config file!")
            exit()

    folder_path = files_config_content["folder_path"]
    return folder_path


def list_file_paths(folder_path):
    """Lists the file paths of all files within a folder."""

    file_paths=[]

    for root, directories, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".org"):  # Check for .org extension
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
    return file_paths  

############################################################
#               org file parsing functions                 #
############################################################

def repeat_parser(repeat_pattern, org_date_time):
    if repeat_pattern == [('+', 1, 'd')]:
        repeater = {'pattern': {'type': 'daily', 'interval': 1, 'month': 0, 'dayOfMonth': 0, 'daysOfWeek': [], 'firstDayOfWeek': 'monday', 'index': 'first'},
                    'range': {'type': 'noEnd', 'startDate': '2005-04-14', 'endDate': '0001-01-01', 'recurrenceTimeZone': 'UTC', 'numberOfOccurrences': 0}
                    }
        repeater["range"]["startDate"] = org_date_time.start.strftime("%Y-%m-%d")
        repeater["pattern"]["interval"] = repeat_pattern[0][1]
        
    elif repeat_pattern == [('+', 1, 'w')]:
        repeater = {'pattern': {'type': 'weekly', 'interval': 1, 'month': 0, 'dayOfMonth': 0, 'daysOfWeek': [], 'firstDayOfWeek': 'monday', 'index': 'first'},
                    'range': {'type': 'noEnd', 'startDate': '2005-04-14', 'endDate': '0001-01-01', 'recurrenceTimeZone': 'UTC', 'numberOfOccurrences': 0}
                    }
        repeater["range"]["startDate"] = org_date_time.start.strftime("%Y-%m-%d")
        repeater["pattern"]["daysOfWeek"] = [strftime("%A").lower()]
        repeater["pattern"]["interval"] = repeat_pattern[0][1]
        
    elif repeat_pattern == [('+', 1, 'm')]:
        repeater = {'pattern': {'type': 'absoluteMonthly', 'interval': 1, 'month': 0, 'dayOfMonth': 0, 'daysOfWeek': [], 'firstDayOfWeek': 'monday', 'index': 'first'},
                    'range': {'type': 'noEnd', 'startDate': '2005-04-14', 'endDate': '0001-01-01', 'recurrenceTimeZone': 'UTC', 'numberOfOccurrences': 0}
                    }
        repeater["range"]["startDate"] = org_date_time.start.strftime("%Y-%m-%d")
        repeater["pattern"]["dayOfMonth"] = org_date_time.day
        repeater["pattern"]["interval"] = repeat_pattern[0][1]



def open_file(file_path):
#    file_path='/home/rajesh/temp/orgparser/temp.org'
    todo_keys = ['TODO', 'NEXT', 'WAITING', 'PROJ']
    done_keys = ['DONE', 'CANCELLED', 'DEFERRED']
    env = OrgEnv(todos=todo_keys, dones=done_keys, filename=file_path)
    root = load(file_path, env=env)
    return root

def is_task(heading):
    '''Return true if a org heading is a todo heading else return false'''
    if heading.todo or heading.has_date():
        return True
    else:
        return False


def has_children(heading):
    ''' Check is a org mode heading has children or not. Return True if
    it is has children, false otherwise'''

    children=heading.children

    if children:
        return True
    else:
        return False

def is_project(heading):
    ''' Return true if the org todo keyword is equal to PROJ or has children, else return false'''

    if heading.todo == "PROJ":
        return True
    else:
        return False

class org_todo:
  def __init__(self, todo, heading, scheduled, deadline, repeat, body, today, remind, closed):
    self.todo = todo
    self.heading = heading
    self.scheduled = scheduled
    self.deadline = deadline
    self.repeat = repeat
    self.body = body
    self.today = today
    self.remind = remind
    self.closed = closed

def org_process_node(node):
    
    if bool(node.todo) == True:
        todo=node.todo
    else:
        todo=""

    if bool(node.heading) == True:
            heading=node.heading
    else:
        title=False

    if bool(node.scheduled) == True and bool(node.scheduled._repeater) == False and bool(node.deadline._repeater) == False:
        scheduled={'dateTime': node.scheduled.start.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': 'UTC'}
        # scheduled=node.scheduled
    else:
        scheduled= False

    if bool(node.deadline) == True:
        deadline={'dateTime': node.deadline.start.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': 'UTC'}
        # deadline=node.deadline
    else:
        deadline= False

    if type((node.has_date())) is list and bool(node.deadline) == False and bool(node.scheduled) == False:
        timestamp_date = node.has_date()[0]
        scheduled={'dateTime': timestamp_date.start.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': 'UTC'}

        if timestamp_date.has_end() is True:
            deadline={'dateTime': timestamp_date.end.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': 'UTC'}

    if bool(node.scheduled._repeater) == True or bool(node.deadline._repeater) == True:
        if bool(node.scheduled._repeater) == True:
            repeat=repeat_parser(node.scheduled._repeater, node.scheduled)
        else:
            repeat=repeat_parser(node.deadline._repeater, node.deadline)
    else:
        repeat=False

    if bool(node.body) == True:
        body=node.body
    else:
        body=False
        
    if node.scheduled.start == datetime.date.today() or node.deadline.start == datetime.date.today():
        today=True
    else:
        today=False

    if node.scheduled or node.deadline:
        remind = True
    else:
        remind = False
    if bool(node.closed) == True:
        closed = {'dateTime': node.closed.start.strftime("%Y-%m-%dT%H:%M:%S"), 'timeZone': 'UTC'}
    else:
        closed=False
    todo= org_todo(todo, heading, scheduled, deadline, repeat, body, today, remind, closed)
    return todo 

