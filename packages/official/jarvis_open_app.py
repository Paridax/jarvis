from subprocess import Popen
import json


def open_app(dictionary):
    if dictionary.get("action") == "open":
        # read list of connected apps from json file
        with open("../../settings/connected_apps.json", "r") as f:
            apps = json.load(f)
        # get the app name
        appname = dictionary.get("appname")
        if appname is None:
            return False
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
                return False
            return True
        else:
            return False
    return False
