from google_interface import Google
from os import system
from re import search, sub
import json
from subprocess import Popen
import datetime
from gtts import gTTS
import playsound
import openai
import os
import dotenv

# Load the environment variables
dotenv.load_dotenv()

# Set the OpenAI API key
API_KEY = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

openai.api_key = API_KEY

# generate directories and log files
# check if directory exists
if not os.path.exists("settings"):
    # if not, create it
    system("mkdir settings")

# if no log file exists, create it
if not os.path.exists("settings/log.txt"):
    with open("settings/log.txt", "w") as f:
        pass

# if no connected apps file exists, create it
if not os.path.exists("settings/connected_apps.json"):
    with open("settings/connected_apps.json", "w") as f:
        pass

# make google search object
google_search = Google()


def wait_then_parse_dictionary(result, prompt, debug=False):
    # access log file and save prompt and response
    with open("settings/log.txt", "a") as f:
        f.write(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {prompt.encode('unicode_escape').decode('utf-8')}\n{result.encode('unicode_escape').decode('utf-8')}\n"
        )
        f.write("\n")

    if debug:
        print("response: ", result)
    # find the dictionary in the response
    # use regex to find the dictionary between { and }
    regex = r"\{[\s\S]*\}"
    dictionary = search(regex, result)
    try:
        # get dictionary as a string
        dictionary = dictionary.group(0)
        # replace double backslashes with single forward slashes
        dictionary = sub(r"\\", "/", dictionary)
        # convert to dictionary
        dictionary = json.loads(dictionary)
        # revert quoted none to none and quoted false to false
        for key in dictionary:
            if dictionary[key] == "None":
                dictionary[key] = None
            if dictionary[key] == "False":
                dictionary[key] = False
    except AttributeError:
        dictionary = {
            "action": "conversation",
            "gptoutput": "There was an error parsing the dictionary. Please try again.",
        }
    return dictionary


def handle_request(message, debug=False, browser="www.google.com"):
    if debug:
        print(f"Asking Jarvis (GPT 3.5 AI Model): {message}")
    else:
        print("Just a moment...")

    prompt = f"""What is the intent of this prompt? Can you give me a JSON OBJECT NOT IN A CODE BLOCK with the keys: "action" (example categories: "conversation","open","query","play","pause"), "weather" (weather related, boolean), location(region name if given), "keywords"(list), "searchcompletetemplateurl", "appname","apppath","websitelink","target","fullsearchquery","songsearch"(song title and author if given, in a string),"openimages"(if the user wants to open google search images),"gptoutput" (your response, leave as null if you are also returning a search query) Make sure to extend any abbreviations, and don't provide context or explanation before giving the dictionary response. Here is the prompt: \"{message}\""""

    result = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=1000,
    )

    text = result["choices"][0]["message"]["content"]

    # only print debug info if debug flag is set
    if debug:
        # print the tokens used
        print(f"Tokens used for completion: {result['usage']['completion_tokens']}")
        print(f"Tokens used for prompt: {result['usage']['prompt_tokens']}")

        # print price of prompt and response in usd
        print(f"Total cost in dollars: ${result['usage']['total_tokens'] * 0.000002}")

    dictionary = wait_then_parse_dictionary(text, prompt, debug=debug)
    # get the action
    action = dictionary.get("action")

    if debug:
        print(f"Action: {action}")
    if action == "conversation":
        print(dictionary.get("gptoutput"))
    # if keywords has added and applist in it then add the app to the connected_apps.json file
    elif "add" in dictionary.get("keywords") and (
        ("app" in dictionary.get("keywords") and "list" in dictionary.get("keywords"))
        or "app list" in dictionary.get("keywords")
        or "applist" in dictionary.get("keywords")
    ):
        # get the app name
        appname = dictionary.get("appname").lower()
        # get the app path
        apppath = dictionary.get("apppath")
        print(f"Adding {appname} to the list of connected apps")
        # print if the connected_apps.json file doesn't exist
        if not os.path.exists("settings/connected_apps.json"):
            print("The connected_apps.json file doesn't exist")
        else:
            print("The connected_apps.json file exists")
        # load the connected_apps.json file using json
        with open("settings/connected_apps.json", "r") as f:
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
    elif dictionary.get("openimages") is True:
        # open the Google search with the fullsearchquery
        print("Opening Google search for", dictionary.get("fullsearchquery"))
        system(
            "start "
            + f"https://{browser}/images?q={dictionary.get('fullsearchquery').replace(' ', '+')}"
        )
    elif action == "open":
        # read list of connected apps from json file
        with open("settings/connected_apps.json", "r") as f:
            apps = json.load(f)
        # get the app name
        appname = dictionary.get("appname")
        if appname is None:
            appname = None
        else:
            appname = appname.lower()
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
            else:
                # get first link from search fullsearchquery
                link = google_search.search(dictionary.get("fullsearchquery"))[0].get(
                    "link"
                )
                print("Opening", link)
                system("start " + link)
    elif action == "play":
        if dictionary.get("websitelink") is not None:
            print("Playing", dictionary.get("websitelink"))
            system("start " + dictionary.get("websitelink"))
        else:
            youtubequery = dictionary.get("songsearch").replace(" ", "+")
            print("Playing", dictionary.get("songsearch"))
            # open the YouTube link
            system(
                "start "
                + f"https://www.youtube.com/results?search_query={youtubequery}"
            )
    elif dictionary.get("weather") is True:
        print("Getting weather...")
        # get the location from the dictionary
        location = dictionary.get("location")
        # get the weather
        weather = google_search.weather(location)
        # print the weather for the day
        print(
            f"""Today's weather in {location}:\nTemperature: {weather["temp"]}°F\nConditions: {weather["weather"]}\nWind Speed: {weather["wind"]}\nHumidity: {weather["humidity"]}\nPrecipitation: {weather["precipitation"]}"""
        )
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
        else:
            query = dictionary.get("fullsearchquery")
            if debug:
                print("Searching for: ", query)
            else:
                print("Searching the web...")

            search_results = google_search.search(query, text=True, links=5)

            prompt = f"""answer the query given using the text given, only give the direct answer, do not repete the question or give background or extra information, it the prompt asks for a link make sure to return one, the text is from a google search of the query, at the end of the text will be links and thier corisponding header text, the query is {query}, the text is {search_results}"""

            response = openai.ChatCompletion.create(
                messages=[
                    {"role": "user", "content": prompt},
                ],
                model="gpt-3.5-turbo",
                temperature=0,
                max_tokens=1000,
            )

            answer = response["choices"][0]["message"]["content"]

            # print price of prompt and response in usd
            if debug:
                print(
                    f"Total cost in dollars: ${response['usage']['total_tokens'] * 0.000002}"
                )

            print(f"ANSWER: {answer}")
