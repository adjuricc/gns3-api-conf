import requests
from netmiko import ConnectHandler

GNS3_SERVER = "http://127.0.0.1:3080"
USERNAME = "admin"
PASSWORD = "KtAtzrSofhocZUwkYF74aXdf5tRIanLfrCVSLLqAKbCfY9ATqSdXEoczKREHBb6W"

# prints a list
def print_list(lst):
    for i in range(len(lst)):
        print(lst[i] + " ")

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

def find_node_id(node_name):
    dict = get_hosts()
    found = False
    for node in dict:
        if(node['name'] == node_name):
            found = True
            print(node['node_id'])
            return node['node_id']
    if(found ==  False):
        print("Could not find the node. Try again.")
        return None

# gets projects on GNS3 server and their settings
def get_projects():
    response = requests.get(f"{GNS3_SERVER}/v2/projects", auth= (USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    return None

# gets hosts of a particular project on GNS3 server and their settings
def get_hosts():
    my_project = input("Enter your project name: ")
    project_id = find_id(my_project)
    header = {"Content-Type": "application/json"}
    response = requests.get(f"{GNS3_SERVER}/v2/projects/{project_id}/nodes", headers=header, auth=(USERNAME, PASSWORD))

    if (response.status_code == 200):
        return response.json()

# all info in formatted style
def see_info(info_list):
    for info in info_list:
        print(info['name'].upper())
        for key, value in info.items():
            print(f"{key}: {value}")
        print("-----------")

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

# creates a new project
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

# creates a new project and lists it with user input
def create_project_user_input():
    new_project_name = input("Enter a name for your new project: ")
    create_project(new_project_name)
    list_project_names()

#deletes a project
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

# prints host names
def print_hostnames():
    my_project = input("Enter your project name: ")
    print("uslo u f")
    project_id = find_id(my_project)
    print("nije puklo u find id")
    header = { "Content-Type": "application/json"}
    response = requests.get(f"{GNS3_SERVER}/v2/projects/{project_id}/nodes", headers= header,auth=(USERNAME, PASSWORD))
    print("nije puklo u response")
    if(response.status_code == 200):
        response = response.json()
        for host in response:
            print(host['name'])

# gets all interfaces
def get_all_interfaces():
    my_project = input("Enter your project name: ")
    router_hostname = input("Enter your router: ")

    project_id = find_id(my_project)
    header = {"Content-Type": "application/json"}

    response = requests.get(f"{GNS3_SERVER}/v2/projects/{project_id}/nodes", headers=header, auth=(USERNAME, PASSWORD))

    if(response.status_code == 200):
        response = response.json()
        for host in response:
            if(host['name'] == router_hostname):
                for key in host['ports']:
                    print(key['name'])

def get_router_config():
    my_project = input("Enter your project name: ")
    project_id = find_id(my_project)

    my_node = input("Enter your node name: ")
    nodes = get_hosts()

    for node in nodes:
        if(node['name'] == my_node):
            print(node['name'])
            cisco_router = {
                "device_type": "cisco_ios",
                "host": node['name'],
                "username": "admin",
                "password": "admin123"}

            with ConnectHandler(**cisco_router) as net_connect:
                result = net_connect.send_command('show hostname')
                net_connect.disconnect()

            print(result)



#def get_active_interfaces():
#    my_project = input("Enter your project name: ")
#    my_device = input("Enter your device name: ")
#
#    project_id = find_id(my_project)
#    header = {"Content-Type": "application/json"}

# starts all devices in topology
def start_all_devices():
    my_project = input("Enter your project name: ")
    project_id = find_id(my_project)

    nodes = get_hosts()

    for node in nodes:
        node_id = node['node_id']
        response = requests.post(f"{GNS3_SERVER}/v2/projects/{project_id}/nodes/{node_id}/start", auth=(USERNAME, PASSWORD))

        if(response.status_code == 200):
            print("Device " + node['name'] + " started successfully.")
        else:
            print("Device " + node['name'] + " failed to start.")

# stops all devices in topology
def stop_all_devices():
    my_project = input("Enter your project name: ")
    project_id = find_id(my_project)

    nodes = get_hosts()

    for node in nodes:
        node_id = node['node_id']
        response = requests.post(f"{GNS3_SERVER}/v2/projects/{project_id}/nodes/{node_id}/stop", auth=(USERNAME, PASSWORD))

        if (response.status_code == 200):
            print("Device " + node['name'] + " stopped successfully.")
        else:
            print("Device " + node['name'] + " failed to stop.")
# main
while(True):
    print("Enter 0 to exit")
    print("Enter 1 to see all projects with their specifications")
    print("Enter 2 to see all project names")
    print("Enter 3 to create a new project")
    print("Enter 4 to delete an existing project")
    print("Enter 5 to change an existing project name")
    print("Enter 6 to print all host names in a particular project")
    print("Enter 7 to see all hosts with their specifications")
    print("Enter 8 to see all interfaces on a specific device")
    print("Enter 9 to start the devices")
    print("Enter 10 to stop the devices")
    print("Enter 11 to see router configuration")
    op = input("Enter an instruction: ")
    match op:
        case "0":
            exit(0)
        case "1":
            see_info(get_projects())
        case "2":
            list_project_names()
        case "3":
            create_project_user_input()
        case "4":
            delete_project()
        case "5":
            change_project_name()
        case "6":
            print_hostnames()
        case "7":
            see_info(get_hosts())
        case "8":
            get_all_interfaces()
        case "9":
            start_all_devices()
        case "10":
            stop_all_devices()
        case "11":
            get_router_config()