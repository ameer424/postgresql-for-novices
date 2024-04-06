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
HEADERS = {'x-api-key': MASTER_KEY}
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

                    hh = {}
                    hh.update(HEADERS)
                    hh.update({'Content-Type': 'application/json'})
                    
                    create_respose = requests.request("POST", url, headers=hh, data=payload)
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

                    # TODO: headers could be cleaned
                    hh = {}
                    hh.update(HEADERS)
                    hh.update({'Content-Type': 'application/json'})

                    create_respose = requests.request("POST", url, headers=hh, data=payload)
                    print(create_respose.json())

                    # TODO: present data 

# -------------------------SETAPI-----------------------------
                case "setapi":
                    url = URL + "ApiState"
                    if not len(raw_command) > 1:
                        print("delete [ID]")
                        continue

# -------------------------NOCASE-----------------------------
                case _:
                    print("Command not found. Avaiable commands are:")
                    print(COMMAND_LIST)

                

if __name__ == "__main__":
    main()

