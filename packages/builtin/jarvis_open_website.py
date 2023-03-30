from os import system
from backend import speak_message

prompt_extension = """"open_website" (necessary fields; websiteUrl: string (full url), websiteName, string, searchQuery: string (query that can be used to find website),"""


def open_website(dictionary, settings):
    if dictionary.get("websiteUrl") is not None:
        print("Opening", dictionary.get("websiteUrl"), "in your browser.")
        system("start " + dictionary.get("websiteUrl"))
    else:
        if dictionary.get("searchQuery") is None:
            return False
        # get first link from search fullsearchquery
        link = settings["google_search"].search(dictionary.get("searchQuery"))[0][
            "link"
        ]
        speak_message(f"Opening {link}", out_loud=settings["out_loud"])
        system("start " + link)
