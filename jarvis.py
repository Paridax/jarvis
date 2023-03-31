import sys

# GLOBAL VARIABLES

flagsData = [
    ("--debug", "Run in debug mode"),
    ("--speak", "Speak the response"),
]

commandsData = [
    ("text", "Run in text mode (default)"),
    ("voice", "Run in voice mode"),
    ("help", "Display this help message"),
]

flagList = {}


# GLOBAL FUNCTIONS


def help_screen():
    print("\nJarvis.py CLI Tool - Created by Paridax and DarkEden\n")
    print("GitHub: https://github.com/paridax/jarvis\n")
    print("Usage:")
    print("python jarvis.py (command) [options]\n")
    print("Commands:")
    for command, description in commandsData:
        print(f"  {command:<10} {'':<3} {description}")
    print("\nOptions:")
    for flag, description in flagsData:
        print(f"  {flag:<10} {'':<3} {description}")
    print("\nExamples:")
    print("python jarvis.py")
    print("python jarvis.py voice")
    print("python jarvis.py text --debug")
    print("python jarvis.py help")
    print("")


def register_flag(flag, description):
    flagsData.append((flag, description))


def register_command(command, description):
    commandsData.append((command, description))


def is_debugging():
    return flagList.get("debug", False)


def is_enabled(flag):
    return flagList.get(flag, False)


# default settings
mode = "text"

# check for command line arguments
if len(sys.argv) > 1:
    command = sys.argv[1]
    args = sys.argv[2:]

    # check that there are no duplicate arguments
    if len(args) != len(set(args)):
        print("Error: Duplicate arguments")
        help_screen()
        sys.exit(1)

    # check for help command
    if command == "help":
        help_screen()
        sys.exit(0)
    # check for text command
    elif command == "text" or command == "voice":
        mode = command
    # check for invalid command
    else:
        print("Error: Invalid command " + command)
        help_screen()
        sys.exit(1)

    # valid args
    valid_args = [flag[0] for flag in flagsData]

    # check for flags
    for arg in args:
        if arg not in valid_args:
            print("Error: Invalid argument " + arg)
            help_screen()
            sys.exit(1)
        if arg.startswith("--"):
            flagList[arg[2:]] = True
        else:
            print("Error: Invalid argument")
            help_screen()
            sys.exit(1)


print("Waking up Jarvis...")

from voice_interface import voice_interface
from text_interface import text_interface
from backend import speak_message

speak_message("How may I help you?", out_loud=is_enabled("speak"))

if mode == "voice":
    voice_interface(is_debugging(), is_enabled("speak"))
elif mode == "text":
    text_interface(is_debugging(), is_enabled("speak"))
