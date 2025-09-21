import graphapi.wrapper as wrapper
import orgutils.utils as utils
import os

# make folder config file and return a list of file paths
config_dir = utils.make_config()
folder_path = utils.make_folder_config_and_return_folder_path(config_dir)
output_file_paths = utils.list_file_paths(folder_path)
excluded_files = ["someday.org", "archives.org", "review.org",
                  "corevalue-goals.org", "corevalue-action-plan.org"]
file_paths = [file_path for file_path in output_file_paths if all(
    excluded_file not in file_path for excluded_file in excluded_files)]
print(file_paths)

# purge existing microsoft todo tasks and lists
for files in file_paths:
    list_name = os.path.basename(files)
    print(list_name)
    try:
        list_id = wrapper.get_list(list_name)
    except IndexError:
        print(f"no list with name: {list_name}")
    else:
        wrapper.delete_list(list_id)

# delete existing projects list
try:
    project_id = wrapper.get_list("Projects")
except IndexError:
    print(f"no list with name: {list_name}")
else:
    wrapper.delete_list(project_id)


# make a projects list
project_list = wrapper.create_project_list()

# create new lists and tasks
for files in file_paths:
    print(files)
    root = utils.open_file(files)
    list_name = os.path.basename(files)
    list_id = wrapper.create_list(list_name)

    for i in root[1:]:
        if utils.is_task(i):
            print(i)
            if utils.is_project(i):
                project_tasks = i.children
                head_project_node = utils.org_process_node(i)
                wrapper.create_task(head_project_node, project_list)
                for x in project_tasks:
                    children_project_node = utils.org_process_node(x)
                    wrapper.create_project_task(
                        head_project_node, children_project_node, list_id)
            else:
                parent = i.get_parent()
                if utils.is_project(parent):
                    continue
                else:
                    task = utils.org_process_node(i)
                    wrapper.create_task(task, list_id)
