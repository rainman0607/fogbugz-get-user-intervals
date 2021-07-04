from sys import argv
from lib.get.main import *

commands = {
    "t": getToday(),
    "w": getWeek(),
    "m": getMonth(),
    "a": getAll(),
    "missing": getMissing(),
}

if len(argv) == 2:
    if argv[1] in commands:
        print(commands[argv[1]])
    elif argv[1] == "setup":
        print(setup())
    else:
        print("Command not found!")
else:
    print("You need to specify a command.")
