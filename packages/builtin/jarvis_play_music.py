from os import system
from backend import speak_message


def play_music(dictionary, settings):
    if dictionary["action"] == "play":
        if dictionary.get("websitelink") is not None:
            print("Playing", dictionary.get("websitelink"), "in your browser.")
            if settings["debug"]:
                print(f"""Playing: {dictionary.get("websitelink")}""")
            speak_message(
                "Opening the link in your browser...", out_loud=settings["out_loud"]
            )
            system("start " + dictionary.get("websitelink"))
        else:
            # get the first link on google for the search and open it
            link = (
                settings["google_search"]
                .search(dictionary.get("songsearch"))[0]
                .get("link")
            )
            if settings["debug"]:
                print(f"Playing: {link}")
            speak_message(
                "Opening the link in your browser...", out_loud=settings["out_loud"]
            )
            # open the link using system
            system("start " + link)
        return True
    return False
