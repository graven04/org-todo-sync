import graphapi.graphapi as graphapi
import graphapi.wrapper as wrapper
import orgutils.utils as utils
import os



# make folder config file and return a list of file paths
folder_path = utils.make_folder_config_and_return_folder_path()
output_file_paths = utils.list_file_paths(folder_path)
excluded_files = ["someday.org", "archives.org"]
file_paths = [file_path for  file_path in output_file_paths if all(excluded_file not in file_path for excluded_file in excluded_files)]
print(file_paths)

# purge existing microsoft todo tasks and lists
lists = wrapper.get_lists()
wrapper.purge_lists(lists)

# make a projects list
project_list = wrapper.create_project_list()

# create new lists and tasks
for files in file_paths:
    print(files)
    root=utils.open_file(files)
    list_name = os.path.basename(files)
    list_id=wrapper.create_list(list_name)

    
    for i in root[1:]:
        if utils.is_task(i):
            print(i)
            if utils.is_project(i):
                project_tasks = i.children
                head_project_node = utils.org_process_node(i)
                wrapper.create_task(head_project_node, project_list)
                for x in project_tasks:
                    children_project_node = utils.org_process_node(x)
                    wrapper.create_project_task(head_project_node, children_project_node, list_id) 
            else:
                task = utils.org_process_node(i) 
                wrapper.create_task(task,list_id)












    # for i in root[1:]:
    #     node = utils.org_process_node(i)
    #     if utils.is_task(node):
        
    #         if utils.is_project(node) then:
    #             wrapper.create_project(node,list_id) 
    #         else:
    #             wrapper.create_task(node,list_id)


''' for projects, i was thinking:
- if the task is part of a project then make a task in the form: " { project name } || { task name }"
'''
