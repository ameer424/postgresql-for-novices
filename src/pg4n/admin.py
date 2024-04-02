
command_list = ["help", "exit"]

def main():
    while(True):
        command = input("Enter command: ")
        match command:
            case "help":
                print(command_list)
            case "exit":
                break
            case _:
                print("Command not found. Avaiable commands are:")
                print(command_list)
    


if __name__ == "__main__":
    main()

