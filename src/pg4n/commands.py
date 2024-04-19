# Admin functionality and control of pg4n cloud implementations.
import json
import os
import os.path
import requests
from .config_reader import ConfigReader
from .config_values import ConfigValues

USER_COMMANDS = ["help", "address", "apikey", "exit"]
ADMIN_COMMANDS =  ["All user commands +", "get", "create", "delete", "setapi","setparams","getparams"]
HELP_TEXT = "All user commands are 1 liners. COMMAND + 1 SPACE + VALUE\Some admin commands aren't."
CONFIG_FILE_NAME = "pg4n.conf"
USERS_FILE_NAME = "pg4n_users.json"

def read_list_input():
    inputs = []
    count = 1
    print("Add 1 ID at time. Leave empty to stop.")
    while True:        
        input_value = input(str(count) + ". ID: ")        
        if input_value == "":
            break
        inputs.append(input_value)
        count = count + 1
    return inputs

def read_input(expected_input_type,input_text,error):
    while True:                  
        input_value = input(input_text)
        try:
            if input_value == "":
                return input_value
            return expected_input_type(input_value)
        except:
            print("Input type is wrong! Needs to be " + error +". Try again!")        

def print_response_json(obj):    
    try:
        if 'message' in obj:
            print(obj['message'])
        else:
            print("ID: " + obj['ID'] 
                + ", Name: " + obj['Name'] 
                + ", Key: " + obj['Key']
                + ", Tokens: " + str(obj['Tokens']))        
    except:        
        print("Missing value in responce!")

def fileIO(file_value, input_value):   

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
    # sets "constants" and checks if values are in file
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
        print("APIKey loaded from file.")
        HEADERS = {'x-api-key': config_values.get("APIKey"),
           'Content-Type': 'application/json'}
        
    if config_values.get("LambdaAddress") is not None:
        print("Address loaded from file.")
        URL = config_values.get("LambdaAddress")

    config_values["LambdaAddress"] = "https://rb7711t55l.execute-api.us-east-1.amazonaws.com/"    
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

            if command != "apikey" and command != "address" and command != 'exit':
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
                    print("")                                       
                    print("User commands: ")
                    print(USER_COMMANDS)                    
                    print("Admin commands: ")
                    print(ADMIN_COMMANDS)
                    print("")
                    print(HELP_TEXT)                                     
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
                    apikey_is_Ok = fileIO("apikey: ",raw_command_split[1])
                    if apikey_is_Ok[0]:                        
                        config_values["APIKey"] = apikey_is_Ok[1]
                        HEADERS = {'x-api-key': apikey_is_Ok[1],
                                    'Content-Type': 'application/json'}                                      

# ----------------------ADDRESS-----------------------------
                case "address":
                    if not len(raw_command_split) == 2:
                        print("address ADDRESS_WANTED_TO_BE_SAVE")
                        continue
                    address_is_Ok = fileIO("address: ",raw_command_split[1])
                    if address_is_Ok[0]:
                        config_values["LambdaAddress"] = address_is_Ok[1] 
                        URL = address_is_Ok[1]

# -------------------------GET-----------------------------
                case "get":
                    makeHttp = True
                    #if not len(raw_command_split) > 1:
                    #    print("get [IDs]")
                    #    continue
                    if len(raw_command_split) == 2 and raw_command_split[1] == "all":
                        url = URL + "getAllKeys"
                    else:
                        readed_inputs = read_list_input()
                        if len(readed_inputs) > 0:                   
                            ids = [str(id) for id in readed_inputs] 
                            #ids = [str(id) for id in raw_command_split[1:]]                        
                            url = URL + "getKeys?id="
                            query = ','.join(ids)
                            url = url + query
                        else:
                            makeHttp = False                   
                    if makeHttp:                        
                        get_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                        
                        res_json = get_response.json()                   
                                            
                        for obj in res_json:
                            print_response_json(obj)
                    else:
                        print("No ID:s to get!")                               
                
# -------------------------CREATE-----------------------------                
                case "create":
                    makeHttp = True
                    url = URL + "createKeys"
                    if not len(raw_command_split) > 1:
                        print("create [ID:NAME]")
                        print("EXAMPLE: create T1:some name, T2:some other name")
                        continue

                    ids = raw_command[7:].split(', ')
                    
                    raw_payload = []
                    for id in ids:
                        nro, name = id.split(':')
                        if nro == "":
                            print("Student ID is missing. Aborting create!")
                            makeHttp = False
                            break
                        if name == "":
                            print("Student name is missing Aborting create!")
                            makeHttp = False
                            break
                        raw_payload.append({"id":nro.strip(), "name":name.strip()})

                    if makeHttp:
                        payload = json.dumps(raw_payload)                    
                        
                        create_response = requests.request("POST", url, headers=HEADERS, data=payload)
                        res_json = create_response.json()
    
                        for obj in res_json:
                            print_response_json(obj)
                    

 # -------------------------DELETE-----------------------------
                case "delete":
                    url = URL + "deleteKeys?id="
                    if not len(raw_command_split) > 1:
                        print("delete [ID]")
                        continue   

                    ids = [str(id) for id in raw_command_split[1:]]
                        
                    url = URL + "deleteKeys?id="
                    query = ','.join(ids)
                    url = url + query                   

                    delete_respose = requests.request("DELETE", url, headers=HEADERS, data=PAYLOAD)
                    res_json = delete_respose.json()
                    
                    for obj in res_json:
                        print_response_json(obj) 

# --------------------------SETAPI-----------------------------
                case "setapi":                    
                    url = URL + "changeApiState"
                    if not len(raw_command_split) == 2:
                        print("setapi ON/OFF")
                        continue

                    set_param = raw_command_split[1]
                    set_param = str(set_param).upper()

                    if not set_param == "ON" and not set_param == "OFF":
                        print("Invalid parameter! The parameter can only be 'ON' or 'OFF'.")
                        continue                        

                    raw_payload = {'apiState':set_param}
                    payload = json.dumps(raw_payload)

                    setapi_response = requests.request("POST", url, headers=HEADERS, data=payload)
                    print(setapi_response.json())

# ---------------------SETPARAMETERS--------------------------
                case "setparams":
                    print("\nGive new parameters. Leave empty if no new value.")
                    
                    input_responce_length = read_input(int,"Responce length: ","Integer")
                    input_temperature = read_input(float,"Temperature: ","Float")
                    input_topP = read_input(float,"TopP: ","Float")
                    input_prompt = read_input(str,"Prompt: ","String")                  

                    url = URL + "parameters"

                    raw_payload = {}

                    if input_responce_length != "":
                        raw_payload['responseLength'] =  input_responce_length
                    if input_temperature != "":
                        raw_payload['temperature'] =  input_temperature
                    if input_topP != "":
                        raw_payload['topP'] =  input_topP
                    if input_prompt != "":
                        raw_payload['modelInstructions'] =  input_prompt    
                                 
                    if input_responce_length == "" and input_temperature == "" and input_topP == "" and input_prompt == "":
                        print("All parameters are empty, no update needed!")                        
                    else:
                        payload = json.dumps(raw_payload)                                               
                        set_parameters_response = requests.request("POST", url, headers=HEADERS, data=payload)
                        if set_parameters_response.status_code == 200:
                            res_json = set_parameters_response.json()
                            print("New parameteres are:")
                            print("Response Length: " + str(res_json['responseLength'])
                                + ", \nTemperature: " + str(res_json['temperature'])
                                + ", \nTopP: " + str(res_json['topP'])
                                + ", \nPrompt: " + res_json['ModelInstructions'])
                        else:
                             res_json = set_parameters_response.json()
                             print(res_json)       

# ---------------------GETPARAMETERS--------------------------
                case "getparams":
                    url = URL + "parameters"

                    get_parameters_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    if get_parameters_response.status_code == 200:
                        res_json = get_parameters_response.json()
                        print("Response Length: " + res_json['responseLength']
                            + ", \nTemperature: " + res_json['temperature']
                            + ", \nTopP: " + res_json['topP']
                            + ", \nPrompt: " + res_json['ModelInstructions'])
                    else:
                             res_json = get_parameters_response.json()
                             print(res_json)                                       

# -------------------------NOCASE-----------------------------
                case _:
                    if not value_not_in_file_error:
                        print("Command not found. Available commands are:")                  
                    print("User commands: ")
                    print(USER_COMMANDS)                    
                    print("Admin commands: ")
                    print(ADMIN_COMMANDS)                                                                     

if __name__ == "__main__":
    main()