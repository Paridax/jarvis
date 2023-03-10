from os import system
from backend import speak_message


def open_image(dictionary, settings):
    # open the Google search with the fullsearchquery
    speak_message(
        "Opening Google search for " + dictionary.get("imagesearch"),
        out_loud=settings["out_loud"],
    )
    system(
        "start "
        + f"""https://{settings["browser"]}/images?q={dictionary.get('imagesearch').replace(' ', '+')}"""
    )
