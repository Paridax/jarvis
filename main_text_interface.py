import dotenv
from backend import backend
import openai
import sys

# Load the environment variables
dotenv.load_dotenv()

# Set the OpenAI API key
API_KEY = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

openai.api_key = API_KEY

# make a command line interface debug flag with sys
debug = False
if len(sys.argv) > 1:
    # check if --debug is in any of the command line arguments
    if "--debug" in sys.argv:
        debug = True
        print("Debug mode enabled")

while True:
    message = input("> ")
    message = message.strip()

    # if the message is empty, don't send it to the API
    if message == "":
        continue

    # send the message to the backend
    backend(message, debug=debug, browser="search.brave.com")
