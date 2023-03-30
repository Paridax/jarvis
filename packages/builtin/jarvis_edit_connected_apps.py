import json
import os

prompt_extension = (
    """("edit_connected_apps" (necessary fields; appPath: string, appName: string)"""
)


def edit_connected_apps(dictionary):
    if "add" in dictionary.get("keywords") and (
        ("app" in dictionary.get("keywords") and "list" in dictionary.get("keywords"))
        or "app list" in dictionary.get("keywords")
        or "applist" in dictionary.get("keywords")
    ):
        # get the app name
        appname = dictionary.get("appName").lower()
        # get the app path
        apppath = dictionary.get("appPath")
        print(f"Adding {appname} to the list of connected apps.")
        # print if the connected_apps.json file doesn't exist
        if not os.path.exists("settings/connected_apps.json"):
            print("The connected_apps.json file doesn't exist.")
        else:
            print("The connected_apps.json file exists.")
        # load the connected_apps.json file using json
        with open("settings/connected_apps.json", "r") as f:
            apps = json.load(f)
        # add the app name and path to the json file
        apps[appname] = apppath
        # save the json file
        with open("settings/connected_apps.json", "w") as f:
            json.dump(apps, f)
        print("Added", appname, "to the list of connected apps.")

    # if keywords has remove and applist in it then remove the app from the connected_apps.json file
    elif "remove" in dictionary.get("keywords") and (
        "applist" in dictionary.get("keywords")
        or "app list" in dictionary.get("keywords")
    ):
        # get the app name
        appname = dictionary.get("appName").lower()
        # open the connected_apps.json file
        with open("settings/connected_apps.json", "r") as f:
            apps = json.load(f)
        # remove the app name and path from the json file
        del apps[appname]
        # save the json file
        with open("settings/connected_apps.json", "w") as f:
            json.dump(apps, f)
        print("Removed", appname, "from the list of connected apps.")
