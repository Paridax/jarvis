import scraper
import dotenv
from os import system
from re import search
import json
from subprocess import Popen
import datetime
from gtts import gTTS
import playsound
import openai

# Load the environment variables
dotenv.load_dotenv()

# Set the OpenAI API key
API_KEY = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

openai.api_key = API_KEY


def wait_then_parse_dictionary(result, prompt):
    # access log file and save prompt and response
    with open("settings/log.txt", "a") as f:
    # write the prompt and response to the log file, encode unicode characters to prevent errors
    f.write(
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {prompt.encode('unicode_escape').decode('utf-8')}\n{result.encode('unicode_escape').decode('utf-8')}\n"
    )
    f.write("\n")

    print("response", result)
    # find the dictionary in the response
    # use regex to find the dictionary between { and }
    regex = r"\{[\s\S]*\}"
    dictionary = search(regex, result)
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
    message = message.strip()

    prompt = f"""What is the intent of this prompt? Can you give me a JSON OBJECT NOT IN A CODE BLOCK with the keys: "action" (example categories: "conversation","open","execute","query","play","pause"), "weather" (weather related, boolean), location(region name if given), "keywords"(list), "searchcompletetemplateurl", "appname","apppath","websitelink","target","fullsearchquery","songsearch"(song title and author if given),"gptoutput" (your response, leave as null if you are also returning a search query) Make sure to extend any abbreviations, and don't provide context or explanation before giving the dictionary response. Here is the prompt: \"{message}\""""

    result = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=1000,
    )

    text = result["choices"][0]["message"]["content"]

    # print the tokens used
    print(f"Tokens used for completion: {result['usage']['completion_tokens']}")
    print(f"Tokens used for prompt: {result['usage']['prompt_tokens']}")

    # print price of prompt and response in usd
    print(f"Total cost in dollars: ${result['usage']['total_tokens'] * 0.000002}")

    dictionary = wait_then_parse_dictionary(text, prompt)
    # get the action
    action = dictionary.get("action")
    print(f"Action: {action}")
    if action == "conversation":
        print(dictionary.get("gptoutput"))
    # if keywords has add and applist in it then add the app to the connected_apps.json file
    elif "add" in dictionary.get("keywords") and (
            ("app" in dictionary.get("keywords") and "list" in dictionary.get("keywords"))
            or "app list" in dictionary.get("keywords")
            or "applist" in dictionary.get("keywords")
    ):
        # get the app name
        appname = dictionary.get("appname").lower()
        # get the app path
        apppath = dictionary.get("apppath")
        # open the connected_apps.json file
        with open("settings/connected_apps.json", "r")as f:  # if the file is empty then make it an empty dictionary
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
    elif action == "play":
        if dictionary.get("websitelink") is not None:
            print("Playing", dictionary.get("websitelink"))
            system("start " + dictionary.get("websitelink"))
        else:
            youtubequery = (
                    dictionary.get("songsearch")["title"].replace(" ", "+")
                    + "+"
                    + dictionary.get("songsearch")["author"].replace(" ", "+")
            )
            print("Playing", dictionary.get("songsearch")["title"])
            # open the youtube link
            system(
                "start "
                + f"https://www.youtube.com/results?search_query={youtubequery}"
            )
    elif dictionary.get("weather") is True:
        print("Getting weather")
        # get the location from the dictionary
        location = dictionary.get("location")
        # get the weather
        weather = scraper.weather(location)
        # print the weather for the day
        print(
            f"""Today's weather in {location}:\nTemperature: {weather["temp"]}°F\nConditions: {weather["weather"]}\nWind Speed: {weather["wind"]} mph\nHumidity: {weather["humidity"]}\nPrecipitation: {weather["precipitation"]}"""
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
            continue
        query = dictionary.get("fullsearchquery")
        url = dictionary.get("searchcompletetemplateurl")
        print("Querying", query)

        search_results = scraper.search(query, two_results=True)

        print(f"Original search result length: {len(search_results)}")
        # take away anything that is unneeded from the search results
        search_results = search_results.replace("<div>", "")
        search_results = search_results.replace("</div>", "")
        search_results = search_results.replace("<tr>", "")
        search_results = search_results.replace("<th>", "")
        search_results = search_results.replace("</th>", "")
        search_results = search_results.replace("<th", "")
        print(f"Search result length after removing divs: {len(search_results)}")

        prompt = f"""Answer the query given the html data given, answer with a json object with an answer key Query:  \"{query}\" HTML: {search_results}"""

        response = openai.ChatCompletion.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=1000,
        )

        text = response["choices"][0]["message"]["content"]

        # print price of prompt and response in usd
        print(f"Total cost in dollars: ${response['usage']['total_tokens'] * 0.000002}")

        dictionary = wait_then_parse_dictionary(text, prompt)

        # get the answer
        answer = dictionary.get("answer")
        print("ANSWER:")
        print(answer)
