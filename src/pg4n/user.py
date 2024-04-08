import os.path

command_list = ["help", "exit","address","apikey"]
CONFIG_FILE_NAME = "pg4n.conf"

def main():
    """
    Starts an infinite while loop that asks the admin for commands.
    """
    while(True):
        command = input("Enter command: ")
        match command:
            case "help":
                print(command_list)
                # ask for additional parameters here.
            case "exit":
                break
            case "apikey":
                fileIO("apikey:")
            case "address":
                fileIO("address:")                
            case _:
                print("Command not found. Available commands are:")
                print(command_list)

def fileIO(file_value):   
    # asks user to give the input value
    input_value = input("Give " + file_value + " ")               
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
    else:
        # Writes value to file and saves it.
        try:
            with open(home_config_path, "w") as config_file:
                config_file.write(file_value + input_value )                            
        except Exception as e:
            print("An error occurred:", e)
    print( file_value[:-1].capitalize() + " added!")                                      

if __name__ == "__main__":
    main()