import scraper
from gptinterface import ChatGPT
from dotenv import load_dotenv
from os import getenv, system
from re import search
import json
from time import sleep
from subprocess import Popen
import datetime
from gtts import gTTS
import playsound

load_dotenv()

DEBUG = False

print("Starting...")

token = getenv("OPENAI_TOKEN")
conversation_id = getenv("CONVERSATION_ID")
headless = False  # currently not working

chat = ChatGPT(token=token, conversation_id=conversation_id, headless=headless)
print("Connecting to OpenAI...")
# wait until chat.ready is True
while not chat.ready:
    pass
print("Connected!")


def wait_then_parse_dictionary():
    """
    Waits until the chat is done generating, then parses the dictionary from the response
    :return:
    """
    while chat.is_generating():
        pass

    sleep(0.5)

    response = chat.last_message().get("text").replace("\n", " ")
    if DEBUG:
        print("response", response)
    # find the dictionary in the response
    # use regex to find the dictionary between { and }
    regex = r"\{[\s\S]*\}"
    dictionary = search(regex, response)
    try:
        # get dictionary as a string
        dictionary = dictionary.group(0)
        # remove the first space character if it exists
        if dictionary[1] == " ":
            dictionary = dictionary[0] + dictionary[2:]
        # replace backslashes with forward slashes
        dictionary = dictionary.replace("\\", "/")
        # convert to dictionary
        dictionary = json.loads(dictionary)
    except AttributeError:
        dictionary = {
            "action": "conversation",
            "gptoutput": "There was an error parsing the dictionary. Please try again.",
        }
    return dictionary


while True:
    message = input("> ")
    if not chat.is_generating() and len(message.strip()) > 0:
        message = message.strip()
        result = chat.send(
            f"""What is the intent of this prompt? Can you give me a JSON OBJECT NOT IN A CODE BLOCK with the keys: "action" (example categories: "conversation","open","execute","query","play","pause"), "weather" (weather related, boolean), "keywords"(list), "searchcompletetemplateurl", "appname","apppath","websitelink","target","fullsearchquery","gptoutput" (your response, leave as null if you are also returning a search query) Make sure to extend any abbreviations, and don't provide context or explanation before giving the dictionary response. Here is the prompt: \"{message}\""""
        )
        sleep(0.5)
        if result is False:
            print("Error sending message")
            continue
        else:
            print("Loading...")
        dictionary = wait_then_parse_dictionary()
        # get the action
        action = dictionary.get("action")
        print(f"Action: {action}")
        if action == "conversation":
            print(dictionary.get("gptoutput"))
        # if keywords has add and applist in it then add the app to the connected_apps.json file
        elif "add" in dictionary.get("keywords") and (
                (
                        "app" in dictionary.get("keywords")
                        and "list" in dictionary.get("keywords")
                )
                or "app list" in dictionary.get("keywords")
                or "applist" in dictionary.get("keywords")
        ):
            # get the app name
            appname = dictionary.get("appname").lower()
            # get the app path
            apppath = dictionary.get("apppath")
            # open the connected_apps.json file
            with open(
                    "settings/connected_apps.json", "r"
            ) as f:  # if the file is empty then make it an empty dictionary
                if f.read() == "":
                    apps = {}
                else:
                    apps = json.load(f)
            # add the app name and path to the json file
            apps[appname] = apppath
            # save the json file
            with open("settings/connected_apps.json", "w") as f:
                json.dump(apps, f)
            print("Added", appname, "to the list of connected apps")

        # if keywords has remove and applist in it then remove the app from the connected_apps.json file
        elif "remove" in dictionary.get("keywords") and (
                "applist" in dictionary.get("keywords")
                or "app list" in dictionary.get("keywords")
        ):
            # get the app name
            appname = dictionary.get("appname").lower()
            # open the connected_apps.json file
            with open("settings/connected_apps.json", "r") as f:
                apps = json.load(f)
            # remove the app name and path from the json file
            del apps[appname]
            # save the json file
            with open("settings/connected_apps.json", "w") as f:
                json.dump(apps, f)
            print("Removed", appname, "from the list of connected apps")

        elif action == "open":
            # read list of connected apps from json file
            with open("settings/connected_apps.json", "r") as f:
                apps = json.load(f)
            # get the app name
            appname = dictionary.get("appname").lower()
            # if the app name is in the list of connected apps then open it
            if appname in apps:
                print(f"Opening {appname} at {apps[appname]}")
                # run the executable and add quotes around the path, using subprocess
                # if open fails then print an error message
                try:
                    Popen([f"{apps[appname]}"])
                except:
                    print(f"Could not open {appname} at {apps[appname]}")
            else:
                if dictionary.get("websitelink") is not None:
                    print("Opening", dictionary.get("websitelink"))
                    system("start " + dictionary.get("websitelink"))
        elif action == "play":
            if dictionary.get("websitelink") is not None:
                print("Playing", dictionary.get("websitelink"))
                system("start " + dictionary.get("websitelink"))
            else:
                print("Playing", dictionary.get("target"))
                # replace the spaces in the command with a plus sign
                youtubequery = dictionary.get("target").replace(" ", "+")
                # open the youtube link
                system(
                    f"start https://www.youtube.com/results?search_query={youtubequery}"
                )
        elif action == "execute":
            print("Executing", dictionary.get("target"))
        elif action == "query":
            if "time" in dictionary.get("keywords"):
                # get the current time and print
                print("The time is", datetime.datetime.now().strftime("%H:%M"))

                # say the time
                tts = gTTS(
                    text=f"The time is {datetime.datetime.now().strftime('%H:%M')}",
                    lang="en",
                )
                tts.save("time.mp3")
                # get current path
                path = os.path.dirname(os.path.abspath(__file__))
                playsound.playsound(f"{path}\\time.mp3")
                os.remove("time.mp3")
                continue
            query = dictionary.get("fullsearchquery")
            url = dictionary.get("searchcompletetemplateurl")
            print("Querying", query)

            search_results = scraper.search(query, two_results=True)
            chat.send(
                f"""What is the answer to this query? Can you give me a JSON OBJECT NOT IN A CODE BLOCK in python with a dictionary with the keys: "releventdata" (list),"appname","websitelink","command","answer" (your response in a full sentence, leave as None if you are also returning a search query) Make sure to extend any abbreviations, and don't provide context or explanation before giving the dictionary response. Query:  \""""
                + query
                + """\" HTML: """
                + search_results
            )
            sleep(0.5)

            dictionary = wait_then_parse_dictionary()

            # get the answer
            answer = dictionary.get("answer")
            if DEBUG:
                print("ANSWER:")
            print(answer)
