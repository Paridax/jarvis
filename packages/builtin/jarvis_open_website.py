from os import system
from backend import speak_message


def open_website(dictionary, settings):
    if dictionary["action"] == "open":
        if dictionary.get("websitelink") is not None:
            print("Opening", dictionary.get("websitelink"), "in your browser.")
            system("start " + dictionary.get("websitelink"))
        else:
            # get first link from search fullsearchquery
            link = settings["google_search"].search(dictionary.get("fullsearchquery"))[
                0
            ]["link"]
            speak_message(f"Opening {link}", out_loud=settings["out_loud"])
            system("start " + link)
        return True
    return False
