from backend import backend
import speech_recognition as sr
import os

# make keyword
keyword = "voice assistant"

# Initialize recognizer
r = sr.Recognizer()
print("Adjusting for ambient noise...")
# Adjust for ambient noise
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)
print("Done adjusting for ambient noise")
r.dynamic_energy_threshold = False

# make connected_apps.json in settings folder if it doesn't exist
if not os.path.exists("settings/connected_apps.json"):
    with open("settings/connected_apps.json", "w") as f:
        f.write("{}")

# make a command line interface debug flag with sys
debug = False
if len(sys.argv) > 1:
    # check if --debug is in any of the command line arguments
    if "--debug" in sys.argv:
        debug = True
        print("Debug mode enabled")

while True:
    text = listen_for_key_phrase(keyword, r)

    message = text.lower().replace(keyword, "").strip()

    # if the message is empty, don't send it to the API
    if message == "":
        continue

    # send the message to the backend
    backend(message, debug=debug)
