#
# Firecat's birthday task code
#

import os
names = []
birthdays = []


def get_cmd():
    cmd = input()
    if cmd:
        return cmd.split(" ")
    else:
        print("Please enter something as a command.\n")
        return


def exe_cmd(cmd):
    base_cmd = cmd[0]
    if base_cmd == "help":
        print("help: shows this list\nadd [name] [birthday]: adds [name]'s birthday as [birthday]\nremove [name]: "
              "removes [name]'s birthday\nget birthday [name]: shows [name]'s birthday\nget name [birthday]: shows "
              "whose birthday is [birthday] - can return multiple names\nprint file [path]: prints all birthday data "
              "into a txt file at [program location]/path\nprint console: prints all birthday data into the console\n"
              "exit: stops the program\n")
        return 0
    elif base_cmd == "add":
        if len(cmd) == 3:
            names.append(cmd[1])
            birthdays.append(cmd[2])
            return 1
        print("Your command is too long or too short. The add cmd works as follows: \"add [name] [birthday]\".\n")
        return
    elif base_cmd == "remove":
        if len(cmd) == 2:
            if cmd[1] in tuple(names):
                birthdays.remove(birthdays[names.index(cmd[1])])
                names.remove(cmd[1])
                return 1
            print("The person whose birthday you are trying to remove does not exist.\n")
            return
        print("Your command : \"remove [name]\".\n")
        return
    elif base_cmd == "get":
        if len(cmd) == 3:
            if cmd[1] == "birthday":
                if cmd[2] in tuple(names):
                    print(birthdays[names.index(cmd[2])])
                    return 0
                print("The person whose birthday you are trying to get does not exist.\n")
                return
            elif cmd[1] == "name":
                if cmd[2] in tuple(birthdays):
                    print(names[birthdays.index(cmd[2])])
                    return 0
                print("No person has that birthday.\n")
                return
        print("Your command doesn't have the correct length. Please alter the command if you want to get a birthday"
              "(\"get birthday [name]\") or a name(\"get name [birthday]\").\n")
        return
    elif base_cmd == "print":
        if len(cmd) == 2:
            if cmd[1] == "console":
                print_out = []
                for i in range(len(names)):
                    print_out.append(f"{names[i]} - {birthdays[i]}\n")
                print("".join(print_out))
                return 0
        elif len(cmd) == 3:
            if cmd[1] == "file":
                if os.path.isfile(f"{cmd[2]}.txt"):
                    print("This file already exists. The program will not overwrite files.")
                    return
                else:
                    print_out = []
                    for i in range(len(names)):
                        print_out.append(f"{names[i]} - [{birthdays[i]}\n")
                    file = open(f"{cmd[2]}.txt", mode="w", encoding="utf-8")
                    file.write("".join(print_out))
                    file.close()
                    return 1
        print("Please use the command like this: \"print console\" or \"print file [path]\".\n")
        return
    elif base_cmd == "exit" or base_cmd == "stop":
        yes = ["YES", "yes", "ok", "OK", "confirm", "sure", "yeah"]
        inp = input("Are you sure you want to end the program?\n")
        if inp in tuple(yes):
            print("Ending the program...\n")
            return 0
        print("Cancelled ending the program.\n")
        return
    print("That is not a valid command. Type \"help\" to get a list of commands.\n")
    return


def program():
    cmd = get_cmd()
    if cmd:
        exe = exe_cmd(cmd)
        if exe == "end":
            return
        elif exe == 1:
            print("Success!\n")
    program()


print("\nPlease enter a command. To get a list of commands, use \"help\".\n")
program()
