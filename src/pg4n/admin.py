
command_list = ["help", "exit"]

def activate():
    print("API activated")

def deactivate():
    print("API activated")

def main():
    
    while(True):
        command = input("Enter command: ")
        match command:
            case "help":
                print(command_list)
            case "activate":
                activate()
            case "deactivate":
                deactivate()
            case "exit":
                break
            case _:
                print("Command not found. Avaiable commands are:")
                print(command_list)
    


if __name__ == "__main__":
    main()

