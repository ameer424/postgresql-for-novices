import os.path
from os import  getenv

command_list = ["help", "exit","address"]
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
            case "address":
                address = input("Give lambda address: ")               
                cwd = os.getcwd()
                home_config_path = cwd + "/" + CONFIG_FILE_NAME
                if os.path.isfile(home_config_path):                    
                    try:
                        file_lines = []
                        with open(home_config_path, "r") as config_file:
                            for line in config_file:
                                if line.startswith("address:"):
                                    continue
                                else:
                                    file_lines.append(line.strip())
                        file_lines.append("address: " + address )
                        with open(home_config_path, "w") as config_file:
                            config_file.write("\n".join(file_lines) + "\n")                            
                    except Exception as e:
                        print("An error occurred:", e)
                    print("Lambda address updated!")                   
                else:
                    try:
                        with open(home_config_path, "w") as config_file:
                            config_file.write("address: " + address )                            
                    except Exception as e:
                        print("An error occurred:", e)
                    print("Lambda address added!")                                      
            case _:
                print("Command not found. Available commands are:")
                print(command_list)
    


if __name__ == "__main__":
    main()