# Admin functionality and control of pg4n cloud implementations.
from typing import Optional

import json
import os
import os.path
import requests
from .config_reader import ConfigReader
from .config_values import ConfigValues

#from dotenv import load_dotenv

# pip install python-dotenv
# pip3 install requests

#load_dotenv()

ALL_COMMANDS_LIST = ["help","address","apikey", "exit", "get", "scan", "create", "delete", "setapi","setparams","getparams"]
USER_COMMANDS = ["help", "address", "apikey", "exit"]
ADMIN_COMMANDS =  ["help","address","apikey", "exit", "get", "scan", "create", "delete", "setapi","setparams","getparams"]
CONFIG_FILE_NAME = "pg4n.conf"
USERS_FILE_NAME = "pg4n_users.json"

# env variables for development
#TODO: make reading from config file
#URL = os.getenv('URL')
#MASTER_KEY = os.getenv('MASTER_KEY')

# http request constants
#HEADERS = {'x-api-key': "example_master_key_123",
#           'Content-Type': 'application/json'}
#PAYLOAD = {}

def read_input(expected_input_type,input_text):
    while True:                  
        input_value = input(input_text)
        try:
            if input_value == "":
                return input_value;
            return expected_input_type(input_value)
        except:
            print("Input type is wrong! Try again")        

def print_response_json(obj):
    try:
        print("ID: " + obj['ID'] 
            + ", Name: " + obj['Name'] 
            + ", Key: " + obj['Key']
            + ", Tokens: " + str(obj['Tokens']))
    except:
        print(obj['body'][1:-1]
            + ", Statuscode: " + str(obj['statusCode']))

def fileIO(file_value, input_value):   
    # asks user to give the input value
    #input_value = input("Give " + file_value + " ")

    cwd = os.getcwd()

    home_config_path = cwd + "/" + CONFIG_FILE_NAME

    # Checks if there is a config file allready present in this folder.
    # If there is, checks if the file have old value in it and ignores it
    # and takes other lines in a list and adds new value on it and then 
    # saves it. 
    if os.path.isfile(home_config_path):                    
        try:
            file_lines = []

            with open(home_config_path, "r") as config_file:
                for line in config_file:
                    if line.startswith(file_value):
                        continue
                    else:
                        file_lines.append(line.strip())

            file_lines.append(file_value + input_value )

            with open(home_config_path, "w") as config_file:
                config_file.write("\n".join(file_lines) + "\n") 

        except Exception as e:
            print("An error occurred:", e)
            return (False,"")                 
    else:
        # Writes value to file and saves it.
        try:
            with open(home_config_path, "w") as config_file:
                config_file.write(file_value + input_value )

        except Exception as e:
            print("An error occurred:", e)
            return (False,"")
        
    print( file_value[:-1].capitalize() + " added!")
    return (True,input_value) 

def main():
    """
    Starts an infinite while loop that asks the admin for commands.
    """
    # sets constants and checks if values are in file
    config_values: ConfigValues = {}
    HEADERS = {}
    PAYLOAD = {}
    URL = ""

    try:
        config_reader = ConfigReader()
        config_values = config_reader.read()                    
    except Exception as e:        
        config_values = None

    if config_values is None:
        config_values: ConfigValues = {}

    if config_values.get("APIKey") is not None:
        HEADERS = {'x-api-key': config_values.get("APIKey"),
           'Content-Type': 'application/json'}
        
    if config_values.get("LambdaAddress") is not None:
        URL = config_values.get("LambdaAddress")

    config_values["LambdaAddress"] = "https://6snobruz9e.execute-api.us-east-1.amazonaws.com/"
    URL = config_values.get("LambdaAddress")
    config_values["APIKey"] = "example_master_key_123"
    HEADERS = {'x-api-key': config_values.get("APIKey"),
               'Content-Type': 'application/json'}
    
    
    while(True):
            #raw_command = [str(x) for x in input("Enter command: ").split()]
            raw_command = input("Enter command: ")
            command = ""

            # Error value for preventing user/admin to use commands if APIKey and
            # LambdaAddress are not set.
            value_not_in_file_error = False

            if (raw_command != ""):
                raw_command_split = raw_command.split()
                command = raw_command_split[0]

            if command != "apikey" and command != "address":
                if config_values.get("LambdaAddress") is None:
                    print("Error: Address not set!!")
                    value_not_in_file_error = True
                if config_values.get("APIKey") is None:
                    print("Error: Apikey not set!!")
                    value_not_in_file_error = True

            if value_not_in_file_error:                
                print("Cannot do command!")
                command = ""

            match command:
                case "help":
                    print("All commands: ")
                    print(ALL_COMMANDS_LIST)                    
                    print("User commands: ")
                    print(USER_COMMANDS)                    
                    print("Admin commands: ")
                    print(ADMIN_COMMANDS)                    
                    # ask for additional parameters here.

# -------------------------EXIT-----------------------------
                case "exit":
                    print("Shutting down.")
                    break

# -----------------------APIKEY-----------------------------
                case "apikey":
                    if not len(raw_command_split) == 2:
                        print("apikey APIKEY_WANTED_TO_BE_SAVE")
                        continue
                    is_Ok = fileIO("apikey:",raw_command_split[1])
                    if is_Ok[0]:                        
                        config_values["APIKey"] = is_Ok[1]
                        HEADERS = {'x-api-key': config_values.get("APIKey"),
                                    'Content-Type': 'application/json'}                                      

# ----------------------ADDRESS-----------------------------
                case "address":
                    if not len(raw_command_split) == 2:
                        print("address ADDRESS_WANTED_TO_BE_SAVE")
                        continue
                    is_Ok = fileIO("address:",raw_command_split[1])
                    if is_Ok[0]:
                        config_values["LambdaAddress"] = is_Ok[1] 
                        URL = is_Ok[1]

# -------------------------GET-----------------------------
                case "get":
                    if not len(raw_command_split) > 1:
                        print("get [IDs]")
                        continue
                    
                    ids = [str(id) for id in raw_command_split[1:]]
                    
                    url = URL + "GetKey?ID="
                    query = '&ID='.join(ids)
                    url = url + query                   
                    
                    get_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    res_json = get_response.json()

                    for obj in res_json:
                        print_response_json(obj)                         

# -------------------------SCAN-----------------------------
                case "scan":                   
                    url = URL + "Scan"                        
                    scan_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    res_json = scan_response.json()
                    if len(raw_command_split) == 2 and raw_command_split[1] == "tofile":
                        cwd = os.getcwd()

                        home_config_path = cwd + "/" + USERS_FILE_NAME 
                        try:
                            with open(home_config_path, "w") as users_file:
                                json.dump(res_json, users_file)                                
                        except Exception as e:
                            print("An error occurred:", e)
                    print(res_json)
                    for obj in res_json:
                        print_response_json(obj)                    
                
# -------------------------CREATE-----------------------------                
                case "create":
                    url = URL + "CreateKey"
                    if not len(raw_command_split) > 1:
                        print("create [ID:NAME]")
                        print("EXAMPLE: create T1:some name, T2:some other name")
                        continue

                    ids = raw_command[7:].split(', ')
                    
                    raw_payload = []
                    for id in ids:
                        nro, name = id.split(':')
                        #TODO: add error handling when no nro or name is given
                        #TODO: strip the commands from white spaces before first name
                        raw_payload.append({"ID":nro, "Name":name})
                    payload = json.dumps(raw_payload)
                    #print(payload)
                    
                    create_respose = requests.request("POST", url, headers=HEADERS, data=payload)
                    res_json = create_respose.json()
 
                    for obj in res_json:
                        print_response_json(obj)  

 # -------------------------DELETE-----------------------------
                case "delete":
                    url = URL + "DeleteKey"
                    if not len(raw_command_split) > 1:
                        print("delete [ID]")
                        continue
                    
                    ids = [str(id) for id in raw_command_split[1:]]
                    
                    raw_payload = []
                    for id in ids:
                        raw_payload.append({"ID":id})
                    payload = json.dumps(raw_payload)

                    delete_respose = requests.request("DELETE", url, headers=HEADERS, data=payload)
                    res_json = delete_respose.json()

                    
                    for obj in res_json:
                      print_response_json(obj)   

# --------------------------SETAPI-----------------------------
                case "setapi":                    
                    url = URL + "ApiState"
                    if not len(raw_command_split) == 2:
                        print("setapi ON/OFF")
                        continue

                    set_param = raw_command_split[1]
                    set_param = str(set_param).upper()

                    if not set_param == "ON" and not set_param == "OFF":
                        print("Invalid parameter! The parameter can only be 'ON' or 'OFF'.")
                        continue                        

                    raw_payload = {'SetApiState':set_param}
                    payload = json.dumps(raw_payload)

                    setapi_respose = requests.request("POST", url, headers=HEADERS, data=payload)
                    print(setapi_respose.json())

# ---------------------SETPARAMETERS--------------------------
                case "setparams":
                    print("\nGive new parameters. Leave empty if no new value.")
                    
                    input_responce = read_input(int,"Responce length: ")
                    input_temperature = read_input(float,"Temperature: ")
                    input_topP = read_input(float,"TopP: ")
                    input_prompt = read_input(str,"Prompt: ")                  

                    url = URL + "parameters"
                    raw_payload = {'ResponseLength': input_responce,
                                   'Temperature': input_temperature,
                                   'TopP': input_topP,
                                   'Prompt': input_prompt,
                                   }
                    if input_responce == "" and input_temperature == "" and input_topP == "" and input_prompt == "":
                        print("All parameters are empty, no update needed!")                        
                    else:
                        payload = json.dumps(raw_payload)
                        print(payload)
                        #set_parameters_response = requests.request("POST", url, headers=HEADERS, data=payload)
                        #print(set_parameters_response.json())              

# ---------------------GETPARAMETERS--------------------------
                case "getparams":
                    url = URL + "parameters"

                    get_parameters_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)

                    print(get_parameters_response)
                    res_json = get_parameters_response.json()       
                    print(res_json)
                    #for obj in res_json:
                    #    print_response_json(obj)

# -------------------------NOCASE-----------------------------
                case _:
                    if not value_not_in_file_error:
                        print("Command not found. Available commands are:")
                    print("All commands: ")
                    print(ALL_COMMANDS_LIST)                    
                    print("User commands: ")
                    print(USER_COMMANDS)                    
                    print("Admin commands: ")
                    print(ADMIN_COMMANDS)                                                                     

if __name__ == "__main__":
    main()