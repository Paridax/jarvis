from backend import handle_request
import speech_recognition as sr
import os


def voice_interface(debug, speak):
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

    def listen_for_key_phrase(key_phrase, r):
        print(f"Listening for key phrase {key_phrase}...")
        if debug:
            print(f"Listener energy threshold: {r.energy_threshold}")
        # Use microphone as source
        with sr.Microphone() as source:
            while True:
                try:
                    # Listen for speech
                    audio = r.listen(source, timeout=1, phrase_time_limit=10)

                    try:
                        # Recognize speech using Google Speech Recognition
                        text = r.recognize_google(audio)
                        if debug:
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

        print("You asked: " + text)

        message = text.lower().replace(keyword, "").strip()

        # if the message is empty, don't send it to the API
        if message == "":
            continue

        # send the message to the backend
        handle_request(message, debug=debug, speak=speak)
