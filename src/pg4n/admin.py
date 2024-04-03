
command_list = ["help", "exit"]

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
            case _:
                print("Command not found. Avaiable commands are:")
                print(command_list)
    


if __name__ == "__main__":
    main()

