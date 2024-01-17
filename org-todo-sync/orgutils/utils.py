from orgparse import load, loads
from orgparse import OrgEnv
import os
import yaml # pip install pyyaml



def make_config():
    '''make a config direectory if it doesn't exist already'''
    config_dir = "{}/.config/org-todo-sync".format(os.path.expanduser("~"))
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

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


class org_todo:
    ''' class for a org heading node with attributes '''
  def __init__(self, todo, heading, scheduled, deadline, repeat, body, today):
    self.todo = todo
    self.heading = heading
    self.scheduled = scheduled
    self.deadline = deadline
    self.repeat = repeat
    self.body = body
    self.today = today

def org_process_node(heading):
''' process org node/heading and return a class that contains the node/heading with org heading attributes '''    
    if bool(heading.todo) == True:
        todo=heading.todo
    else:
        todo=False

    if bool(heading.heading) == True:
            heading=heading.heading
    else:
        title=False

    if bool(heading.scheduled) == True and bool(heading.scheduled.__dict__['_repeater']) == False and bool(heading.deadline.__dict__['_repeater']) == False:
        scheduled=heading.scheduled
    else:
        scheduled=False

    if bool(heading.deadline) == True:
        deadline=heading.deadline
    else:
        deadline=False

    if bool(heading.scheduled.__dict__['_repeater']) == True or bool(heading.deadline.__dict__['_repeater']) == True:
        if bool(heading.scheduled.__dict__['_repeater']) == True:
            repeat=heading.scheduled.__dict__['_repeater']
        else:
            repeat=heading.deadline.__dict__['_repeater']
    else:
        repeat=False

    if bool(heading.body) == True:
        body=heading.body
    else:
        body=False
        
    if heading.scheduled.__dict__['_start']== datetime.date.today() or heading.deadline.__dict__['_start'] == datetime.date.today():
        today=True
    else:
        today=False
 
    todo= org_todo(todo, heading, scheduled, deadline, repeat, body, today)
    return todo 


def open_file(file_paths):
    file_path='/home/rajesh/temp/orgparser/temp.org'
    todo_keys = ['TODO', 'NEXT', 'WAITING', 'PROJ']
    done_keys = ['DONE', 'CANCELLED', 'DEFERRED']
    env = OrgEnv(todos=todo_keys, dones=done_keys, filename=file_path)
    root = load(file_path, env=env)
    return root

def is_task(heading):
    '''Return true if a org heading is a todo heading else return false'''
    if heading.todo or heading.scheduled or heading.deadline or heading.get_timestamps():
        return True
    else:
        return False


def has_children(heading):
    ''' Check is a org mode heading has children or not. Return True if
    it is has children, false otherwise'''

    children=org_file[n].children

    if children:
        return True
    else:
        return False

def is_project(heading):
    ''' Return true if the org todo keyword is equal to PROJ, else return false'''

    if heading.todo:
        return True
    else:
        return False
