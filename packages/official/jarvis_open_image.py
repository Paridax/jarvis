from os import system
from backend import speak_message


def open_image(dictionary, settings):
    if dictionary.get("openimages") is True:
        # open the Google search with the fullsearchquery
        speak_message(
            "Opening Google search for " + dictionary.get("fullsearchquery"),
            out_loud=settings["out_loud"],
        )
        system(
            "start "
            + f"""https://{settings["browser"]}/images?q={dictionary.get('fullsearchquery').replace(' ', '+')}"""
        )
        return True
    return False
