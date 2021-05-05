from sys import argv
from lib.get.main import *

if len(argv) == 1 or argv[1] == "t":
    print(getToday())

if len(argv) != 1 and argv[1] == "w":
    print(getWeek())


if len(argv) != 1 and argv[1] == "m":
    print(getMonth())


if len(argv) != 1 and argv[1] == "a":
    print(getAll())


if len(argv) != 1 and argv[1] == "missing":
    print(getMissing())

