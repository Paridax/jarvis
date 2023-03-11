from os import system
from backend import speak_message


def play_music(dictionary, settings):
    # get the first link on google for the search and open it
    link = (
        settings["google_search"]
        .search(f"""{dictionary.get("songName")} -{dictionary.get("artist")} song""")[0]
        .get("link")
    )
    if settings["debug"]:
        print(f"Playing: {link}")
    speak_message("Opening the link in your browser...", out_loud=settings["out_loud"])
    # open the link using system
    system("start " + link)
