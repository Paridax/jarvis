import scraper
from gptinterface import ChatGPT
from time import sleep
from dotenv import load_dotenv
from os import getenv, system
from re import search
import json

load_dotenv()

DEBUG = False

print("Starting...")

token = getenv("OPENAI_TOKEN")
conversation_id = getenv("CONVERSATION_ID")

chat = ChatGPT(token)
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
        # convert dictionary to a python dictionary
        dictionary = json.loads(dictionary)
    except AttributeError:
        dictionary = {"action":"conversation","gptoutput": "There was an error parsing the dictionary. Please try again."}
    return dictionary


while True:
    message = input("> ")
    if not chat.is_generating() and len(message.strip()) > 0:
        message = message.strip()
        result = chat.send(f"""What is the intent of this prompt? Can you give me a JSON OBJECT NOT IN A CODE BLOCK with the keys: "action" (example categories: "conversation","open","execute","query","play","pause"), "weather" (weather related, boolean), "keywords"(list), "searchcompletetemplateurl", "appname","websitelink","target","fullsearchquery","gptoutput" (your response, leave as null if you are also returning a search query) Make sure to extend any abbreviations, and don't provide context or explanation before giving the dictionary response. Here is the prompt: \"{message}\"""")
        sleep(0.5)
        if result is False:
            print("Error sending message")
            continue
        else:
            print("Loading...")
        dictionary = wait_then_parse_dictionary()

        # get the action
        action = dictionary.get("action")
        if action == "conversation":
            print(dictionary.get("gptoutput"))
        elif action == "open":
            print("Opening", dictionary.get("appname"))
            if dictionary.get("websitelink") is not None:
                print("Opening", dictionary.get("websitelink"))
                system("start " + dictionary.get("websitelink"))
        elif action == "play":
            if dictionary.get("websitelink") is not None:
                print("Playing", dictionary.get("websitelink"))
                system("start " + dictionary.get("websitelink"))
        elif action == "execute":
            print("Executing", dictionary.get("target"))
        elif action == "query":
            query = dictionary.get("fullsearchquery")
            url = dictionary.get("searchcompletetemplateurl")
            print("Querying", query)

            search_results = scraper.search(query, two_results=True)
            chat.send(f"""What is the answer to this query? Can you give me a JSON OBJECT NOT IN A CODE BLOCK in python with a dictionary with the keys: "releventdata" (list),"appname","websitelink","command","answer" (your response in a full sentence, leave as None if you are also returning a search query) Make sure to extend any abbreviations, and don't provide context or explanation before giving the dictionary response. Query:  \"""" + query + """\" HTML: """ + search_results)
            sleep(0.5)

            dictionary = wait_then_parse_dictionary()

            # get the answer
            answer = dictionary.get("answer")
            if DEBUG:
                print("ANSWER:")
            print(answer)