import sys


def help_screen():
    print("\nJarvis.py Help Menu - Created by Paridax and DarkEden\n")
    print("GitHub: https://github.com/paridax/jarvis\n")
    print("Usage:")
    print("python jarvis.py [options]\n")
    print("Options:")
    print("  --text         Run in text mode (default)")
    print("  --voice        Run in voice mode")
    print("  --debug        Run in debug mode")
    print("  --speak        Speak the response")
    print("  help           Display this help message\n")
    print("Examples:")
    print("python jarvis.py")
    print("python jarvis.py --voice")
    print("python jarvis.py --text --debug")
    print("python jarvis.py help\n")


# default settings
debug = False
voice_mode = False
text_mode = True
speak = False

# check for command line arguments
if len(sys.argv) > 1:
    if "help" in sys.argv:
        help_screen()
        sys.exit()

    for arg in sys.argv[1:]:
        if arg not in ["--voice", "--text", "--debug", "--speak", "help"]:
            print(f"Unknown argument: {arg}")
            help_screen()
            sys.exit()

    if "--voice" in sys.argv:
        print("Running in voice mode")
        voice_mode = True
        text_mode = False
    elif "--text" in sys.argv:
        print("Running in voice mode")
        text_mode = True
        voice_mode = False
    if "--debug" in sys.argv:
        print("Running in debug mode")
        debug = True
    if "--speak" in sys.argv:
        print("Running in speak mode")
        speak = True

print("Waking up Jarvis...")

from voice_interface import voice_interface
from text_interface import text_interface
from backend import speak_message

speak_message("How may I help you?", out_loud=speak)

if voice_mode:
    voice_interface(debug, speak)
elif text_mode:
    text_interface(debug, speak)
