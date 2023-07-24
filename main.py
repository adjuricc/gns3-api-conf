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
    found = False
    for project in dict:
        if(project['name'] == project_name):
            found = True
            return project['project_id']
    if(found ==  False):
        print("Could not find the project. Try again.")
        return None

# changes the project name
def change_project_name():
    old_project_name = input("Enter the name of the project you want to change: ")
    new_project_name = input("Enter a new name for your project: ")
    header = { "Content-Type": "application/json" }
    data = { "name": new_project_name }
    project_id = find_id(old_project_name)

    response = requests.put(f"{GNS3_SERVER}/v2/projects/{project_id}", json= data, headers= header, auth= (USERNAME, PASSWORD))

    if(response.status_code == 200 or response.status_code == 204):
        print("Project name changed successfully.")
        return response.status_code
    else:
        print("Failed to change the project name.")
        return None

# main
while(True):
    print("Enter 0 to exit")
    print("Enter 1 to see all projects with their specifications")
    print("Enter 2 to see all project names")
    print("Enter 3 to create a new project")
    print("Enter 4 to delete an existing project")
    print("Enter 5 to change an existing project name")
    op = input("Enter an instruction: ")
    match op:
        case "0":
            exit(0)
        case "1":
            see_projects(get_projects())
        case "2":
            list_project_names()
        case "3":
            create_project_user_input()
        case "4":
            delete_project()
        case "5":
            change_project_name()