# Admin functionality and control of pg4n cloud implementations.


import json
import os
import requests
from dotenv import load_dotenv

# pip install python-dotenv
# pip3 install requests

load_dotenv()

COMMAND_LIST = ["help", "exit", "get", "scan", "create", "delete", "setapi"]

# env variables for development
#TODO: make reading from config file
URL = os.getenv('URL')
MASTER_KEY = os.getenv('MASTER_KEY')

# http request constants
HEADERS = {'x-api-key': MASTER_KEY,
           'Content-Type': 'application/json'}
PAYLOAD = {}

def main():
    """
    Starts an infinite while loop that asks the admin for commands.
    """
    while(True):
            raw_command = [str(x) for x in input("Enter command: ").split()]
            command = raw_command[0]

            match command:
                case "help":
                    print(COMMAND_LIST)
                    # ask for additional parameters here.

# -------------------------EXIT-----------------------------
                case "exit":
                    print("Shutting down.")
                    break

# -------------------------GET-----------------------------
                case "get":
                    if not len(raw_command) > 1:
                        print("get [IDs]")
                        continue

                    ids = [str(id) for id in raw_command[1:]]
                    
                    url = URL + "GetKey?ID="
                    query = '&ID='.join(ids)
                    url = url + query
                    #print(url)
                    get_respose = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    print(get_respose.json())

                    # TODO: present data 

# -------------------------SCAN-----------------------------
                case "scan":
                    url = URL + "Scan"
                    #print("url: " + url)
                    scan_respose = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    print(scan_respose.json())

                     # TODO: present data 
                
# -------------------------CREATE-----------------------------                
                case "create":
                    url = URL + "CreateKey"
                    if not len(raw_command) > 1:
                        print("create [ID:NAME]")
                        continue

                    ids = [str(id) for id in raw_command[1:]]
                    
                    raw_payload = []
                    for id in ids:
                        nro, name = id.split(':')
                        raw_payload.append({"ID":nro, "Name":name})
                    payload = json.dumps(raw_payload)
                    
                    create_respose = requests.request("POST", url, headers=HEADERS, data=payload)
                    print(create_respose.json())

                    # TODO: present data 

 # -------------------------DELETE-----------------------------
                case "delete":
                    url = URL + "DeleteKey"
                    if not len(raw_command) > 1:
                        print("delete [ID]")
                        continue
                    
                    ids = [str(id) for id in raw_command[1:]]
                    
                    raw_payload = []
                    for id in ids:
                        raw_payload.append({"ID":id})
                    payload = json.dumps(raw_payload)

                    delete_respose = requests.request("POST", url, headers=HEADERS, data=payload)
                    print(delete_respose.json())

                    # TODO: present data 

# -------------------------SETAPI-----------------------------
                case "setapi":
                    url = URL + "ApiState"
                    if not len(raw_command) == 2:
                        print("setapi ON/OFF")
                        continue

                    set_param = raw_command[1]
                    set_param = str(set_param).upper()

                    if not set_param == "ON" and not set_param == "OFF":
                        print("Invalid parameter! The parameter can only be 'ON' or 'OFF'.")
                        continue                        

                    raw_payload = {'SetApiState':set_param}
                    payload = json.dumps(raw_payload)

                    setapi_respose = requests.request("POST", url, headers=HEADERS, data=payload)
                    print(setapi_respose.json())

                    # TODO: present data 

# -------------------------NOCASE-----------------------------
                case _:
                    print("Command not found. Avaiable commands are:")
                    print(COMMAND_LIST)

                

if __name__ == "__main__":
    main()

