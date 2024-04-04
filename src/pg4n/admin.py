# Admin functionality and control of pg4n cloud implementations.


import json
import os
import requests
from dotenv import load_dotenv

# pip install python-dotenv
# pip3 install requests

load_dotenv()

COMMAND_LIST = ["help", "exit", "get"]

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

                case "exit":
                    print("Shutting down.")
                    break

                case "get":
                    if not len(raw_command) > 1:
                        print("get [IDs]")
                        continue
                    try:
                        ids = [str(id) for id in raw_command[1:]]
                        #print(ids)
                    except:
                        print("ID not valid.")
                    
                    url = URL + "GetKey?ID="
                    query = '&ID='.join(ids)
                    url = url + query
                    #print(url)
                    get_respose = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    print(get_respose.text)

                    # TODO: present data 

                case "scan":
                    url = URL + "Scan"
                    #print("url: " + url)
                    scan_respose = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    print(scan_respose.text)

                     # TODO: present data 

                case _:
                    print("Command not found. Avaiable commands are:")
                    print(COMMAND_LIST)
    


if __name__ == "__main__":
    main()

