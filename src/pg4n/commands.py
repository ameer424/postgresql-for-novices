# Admin functionality and control of pg4n cloud implementations.
import json
import os
import csv
import os.path
import requests
from .config_reader import ConfigReader
from .config_values import ConfigValues


USER_COMMANDS = "help, address, apikey, exit"
ADMIN_COMMANDS =  "All user commands + get, create, delete, setapi, setparameters, getparameters, createkeysfromcsv"
HELP_TEXT = ("User commands: help, address, apikey, exit. Admin can also use these.\n"
            "help: shows help page.\n"
            "example use: help\n"
            "address command to set or change LambdaAddres that is needed to use syntax error help.\n"
            "example use: address https://someaddress.amazonaws.com/\n"
            "apikey: command set or change users apikey that identifies user.\n"
            "example use: apikey kl3477k54kl54lk345kl54lk54kl45kl\n"
            "exit: command to exit program.\n"
            "example use: exit\n\n"
            "Admin commands: get, create, delete, setapi, setparameters, getparameters, createkeysfromcsv\n"
            "get: command to get users from database. Can be used to get users by ID or to get all users.\n"           
            "create: command to create new user or users and add them to database.\n"
            "delete: command to delete user or users from database.\n"
            "setapi: command to set api ON or OFF.\n"
            "setparameters: command to change LLM parameters.\n"
            "getparameters: command to get LLM parameters.\n"
            "createkeysfromcsv: command to add users from file.\n"            
            )
CONFIG_FILE_NAME = "pg4n.conf"
SAVE_FILE = "users.csv"

def all_responces_and_print(response):
    """
    Function to check responces http code and
    continue accordingly. Also catches error if
    something weird happens.

    This function is used: get, delete and both create
    paths.

    Args:
        responce: http responce. 
    """
    try:
        if response.status_code == 200:
            res_json = response.json()
            for obj in res_json:
                print_response_json(obj)
        elif response.status_code == 500:
            print("Error in AWS.")
        else:
            res_json = response.json()
            print(res_json["message"])
    except:
        print("Something went wrong!")

def read_list_input(input_type):
    """
    Function that reads inputs on user returns list of wanted
    strings.

    This function is used: create, get and delete paths.

    Args:
        input_type: what is functions call location.

    Returns:
            List of inputs or empty list.

    """
    inputs = []
    count = 1
    print("Add 1 ID at time. Leave empty to stop.")
    if input_type == "create":        
        print("Name is asked in secondline, after enter.")
        while True:        
            id_value = input(str(count) + ". ID: ")        
            if id_value == "":
                break
            name_value = input(str(count) + ". Name: ")            
            inputs.append({"id":id_value.strip(), "name":name_value.strip()})
            count = count + 1
    else:        
        while True:        
            input_value = input(str(count) + ". ID: ")        
            if input_value == "":
                break
            inputs.append(input_value.strip())
            count = count + 1
    return inputs

def read_input(expected_input_type,input_text,error):
    """
    This function reads parameter input and return
    it in expected format.

    Args:
        expected_input_type: What type of input is expected from user
        string, float or integer.
        input_text: String text what tells what value is this time. 
        error: error text to user that tells what type th input should be.
    
        Returns:
                Expected type input value or empty string.
    """
    while True:                  
        input_value = input(input_text)
        try:
            if input_value == "":
                return input_value
            return expected_input_type(input_value)
        except:
            print("Input type is wrong! Needs to be " + error +". Try again!")        

def print_response_json(obj):
    """
    Printing function for get delete and both create functions.
    First if clause is if http is not 200 and is just error message.
    In else after http 200 full info is printed for 1 user in database.

    Args:
        object: containing 1 line of data
    """    
    try:
        if 'message' in obj:
            print(obj['message'])
        else:
            print("ID: " + obj['ID'] 
                + ", Name: " + obj['Name'] 
                + ", Key: " + obj['Key']
                + ", Tokens: " + str(obj['Tokens']))        
    except:        
        print("Something went wrong!")

def fileIO(file_value, input_value):
    """
    Function handling saving Apikey or Lambdaaddres to file or
    replacing old to new.
    Args:
        file_value: string that has "address" or "apikey" text in it.
        input_value: string that has address or apikey value in it
    
    Returns:
            tuple with first argument success or failure and second
            the input value if not failure. If fails empty string.
    """  

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
            config_file.close()
        except Exception as e:
            print("An error occurred:", e)
            return (False,"")                 
    else:
        # Writes value to file and saves it.
        try:
            with open(home_config_path, "w") as config_file:
                config_file.write(file_value + input_value )
            config_file.close()
        except Exception as e:
            print("An error occurred:", e)
            return (False,"")
        
    print( file_value[:-1].capitalize() + " added!")
    return (True,input_value) 

def read_csv(filename):
    """
    Reads a CSV file with two columns.

    Args:
        filename: The path to the CSV file.

    Returns:
        A list of lists, where each inner list represents a row in the CSV file.
        On error, returns None.
    """
    try:
        # Open the CSV file in read mode
        with open(filename, 'r') as csvfile:
            # Create a CSV reader object
            reader = csv.reader(csvfile)

            # Read the data into a list of lists
            data = []
            for row in reader:
                # Check if the row has exactly two columns
                nro, name = row[0].split(';')
                if nro.strip() != "" and name.strip() != "":
                    data.append({"id":nro.strip(), "name":name.strip()})            
            return (True,data)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return (False,"")
    except ValueError as e:
        print(f"Error reading CSV: {e}")
        return (False,"")

def make_csv(response):
    """
    Function that makes users.csv file with all users in database.
    File is always overwritten if it is allready made.

    Args:
        response: http responce that includes users
    """
    try:
        #check responce status
        if response.status_code == 200:            
            data = []
            res_json = response.json()
            # add column headings
            data.append("ID"+";"+"Name"+";"+"Key"+";"+"Tokens")
            # iterate responce json and save data in csv format        
            for obj in res_json:
                data.append(obj['ID']+";"+obj['Name']+";"+obj['Key']+";"+str(obj['Tokens']))
            # get path to save file
            cwd = os.getcwd()
            home_config_path = cwd + "/" + SAVE_FILE
            # save all data to file
            if len(data) > 1:          
                with open(home_config_path, "w") as config_file:
                    config_file.write("\n".join(data) + "\n")
                config_file.close()
                # inform user that saving happened
                print("Users saved tofile: users.csv")
            else:
                print("Database was empty no users saved.")
        elif response.status_code == 500:
            print("Error in AWS.")
            
        else:
            res_json = response.json()
            print(res_json["message"])            
    except:
        print("Something went wrong!")        
    
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

            if command != "apikey" and command != "address" and command != 'exit' and command != 'help':
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
                    print(HELP_TEXT)                                     
                    # ask for additional parameters here.

# -------------------------EXIT-----------------------------
                case "exit":
                    print("Shutting down.")
                    break

# -----------------------APIKEY-----------------------------
                case "apikey":
                    # command should be has 2 "words" and second is the actual key
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
                    # command should be has 2 "words" and second is the actual address
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
                    toFile = False
                    if len(raw_command_split) == 2 and raw_command_split[1] == "all":
                        url = URL + "getAllKeys"
                    elif len(raw_command_split) == 2 and raw_command_split[1] == "tofile":
                        url = URL + "getAllKeys"
                        toFile = True
                    else:
                        readed_inputs = read_list_input("get")
                        if len(readed_inputs) > 0:                   
                            ids = [str(id) for id in readed_inputs]                                                
                            url = URL + "getKeys?id="
                            query = ','.join(ids)
                            url = url + query
                        else:
                            makeHttp = False
                            print("No ID:s to GET!")                  
                    if makeHttp:                        
                        get_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)                       
                        if toFile:
                            try:
                                make_csv(get_response)            
                            except Exception as e:
                                print("An error occurred:", e)
                        else:
                            all_responces_and_print(get_response)                                
              
# -------------------------CREATE-----------------------------                
                case "create":
                    makeHttp = True
                    url = URL + "createKeys"
                    raw_payload = []
                    readed_inputs = read_list_input("create")
                    if len(readed_inputs) == 0:                 
                        makeHttp = False
                        print("No user:s to CREATE!")                 
                          
                    if makeHttp:
                        payload = json.dumps(readed_inputs)                    
                        
                        create_response = requests.request("POST", url, headers=HEADERS, data=payload)
                        all_responces_and_print(create_response)                    

 # -------------------------DELETE-----------------------------
                case "delete":
                    makeHttp = True
                    url = URL + "deleteKeys?id="                    
                    
                    readed_inputs = read_list_input("delete")
                    if len(readed_inputs) > 0:
                        ids = [str(id) for id in readed_inputs]
                            
                        url = URL + "deleteKeys?id="
                        query = ','.join(ids)
                        url = url + query                   

                        delete_response = requests.request("DELETE", url, headers=HEADERS, data=PAYLOAD)                        
                    else:
                        makeHttp = False
                        print("No ID:s to DELETE!")

                    if makeHttp:
                        all_responces_and_print(delete_response)                        

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
                    if setapi_response.status_code == 200:
                        res_json = setapi_response.json()
                        print(res_json["result"])
                    elif setapi_response.status_code == 500:
                        print("Unexpected error in AWS.")
                    else:                        
                        res_json = setapi_response.json()
                        print(res_json["result"])       

# ---------------------SETPARAMETERS--------------------------
                case "setparameters":
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
                        elif set_parameters_response.status_code == 500:
                            print("Error in AWS.")
                        else:
                            res_json = set_parameters_response.json()
                            print(res_json["message"])       

# ---------------------GETPARAMETERS--------------------------
                case "getparameters":
                    url = URL + "parameters"

                    get_parameters_response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
                    if get_parameters_response.status_code == 200:
                        res_json = get_parameters_response.json()
                        print("Response Length: " + res_json['responseLength']
                            + ", \nTemperature: " + res_json['temperature']
                            + ", \nTopP: " + res_json['topP']
                            + ", \nPrompt: " + res_json['ModelInstructions'])
                    elif get_parameters_response.status_code == 500:
                        print("Error in AWS.")
                    else:
                        res_json = get_parameters_response.json()
                        print(res_json["message"])

# ---------------------------CREATEKEYSFROMCSV-------------------------

                case "createkeysfromcsv":
                    print("\nGive new parameters.")
                    try:
                        file_full_path = read_input(str,"CSV file full path: ","String")                    

                        raw_payload = read_csv(file_full_path)
                        if (raw_payload[0]): 
                            url = URL + "createKeys"

                            payload = json.dumps(raw_payload[1])                    
                                
                            create_response = requests.request("POST", url, headers=HEADERS, data=payload)
                            all_responces_and_print(create_response)
                    except:
                        print("Something wrong with file path!")
                    

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