import requests

GNS3_SERVER = "http://127.0.0.1:3080"
USERNAME = "admin"
PASSWORD = "KtAtzrSofhocZUwkYF74aXdf5tRIanLfrCVSLLqAKbCfY9ATqSdXEoczKREHBb6W"

# prints a list
def print_list(lst):
    for i in range(len(lst)):
        print(lst[i] + " ")

# all projects in formatted style
def see_projects(projects_list):
    for project in projects_list:
        print(project['name'].upper())
        for key, value in project.items():
            print(f"{key}: {value}")
        print("-----------")

# gets projects on GNS3 server and their settings

def get_projects():
    response = requests.get(f"{GNS3_SERVER}/v2/projects", auth= (USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    return None

# gets only the names of existing projects
def list_project_names():
    projects = []
    response = requests.get(f"{GNS3_SERVER}/v2/projects", auth= (USERNAME, PASSWORD))
    if(response.status_code == 200):
        response = response.json()
        for key in response:
            projects.append(key['name'])
        print_list(projects)
    else:
        print("Error found.")


# creating a new project
def create_project(project_name):
    header = { "Content-Type" : "application/json" }
    data = { "name": project_name }

    response = requests.post(f"{GNS3_SERVER}/v2/projects", json= data, headers= header,auth= (USERNAME, PASSWORD))
    if(response.status_code == 201):
        print("New project successfully created!")
        return response.status_code
    else:
        print("Failed to create a new project.")
        return None

# creating a new project and listing it with user input
def create_project_user_input():
    new_project_name = input("Enter a name for your new project: ")
    create_project(new_project_name)
    list_project_names()

#delete a project

def delete_project():
    project_name = input("Enter a project you want to delete: ")
    project_id = find_id(project_name)
    response = requests.delete(f"{GNS3_SERVER}/v2/projects/{project_id}", auth=(USERNAME, PASSWORD))
    if(response.status_code == 200 or response.status_code == 204):
        print("Project deleted successfully.")
        return response.status_code
    else:
        print("Failed to delete the project.")
        return None

# finds the project id using project name
def find_id(project_name):
    dict = get_projects()
    for project in dict:
        if(project['name'] == project_name):
            return project['project_id']

# main

#list_project_names()
#see_projects(get_projects())
#create_project_user_input()
#see_projects(get_projects())
#delete_project()
list_project_names()