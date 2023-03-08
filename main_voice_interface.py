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


def listen_for_key_phrase(key_phrase, r):
    # Use microphone as source
    with sr.Microphone() as source:
        while True:
            try:
                print("Listening for key phrase...")
                print(f"Listener energy threshold: {r.energy_threshold}")
                # Listen for speech
                audio = r.listen(source, timeout=1, phrase_time_limit=10)

                try:
                    # Recognize speech using Google Speech Recognition
                    text = r.recognize_google(audio)
                    print(f"You said: {text}")

                    # Check if key phrase is in recognized text
                    if key_phrase in text.lower():
                        print(f"Key phrase '{key_phrase}' recognized")
                        # find the end index of the key phrase
                        end_index = text.lower().find(key_phrase) + len(key_phrase)
                        # return the text after the key phrase
                        return text[end_index:]
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(
                        f"Could not request results from Google Speech Recognition service; {e}"
                    )
            except sr.WaitTimeoutError:
                print("Timeout")


while True:
    text = listen_for_key_phrase(keyword, r)

    message = text.lower().replace(keyword, "").strip()

    # if the message is empty, don't send it to the API
    if message == "":
        continue

    # send the message to the backend
    backend(message, debug=debug)
