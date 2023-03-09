from backend import speak_message


def get_weather(dictionary, settings):
    if dictionary["weather"]:
        print("Getting weather...")
        # get the location from the dictionary
        location = dictionary.get("location")
        # get the weather
        weather = settings["google_search"].weather(location)
        # print the weather for the day
        speak_message(f"Today's weather in {location}", out_loud=settings["out_loud"])
        print(
            f"""Today's weather in {location}:\nTemperature: {weather["temp"]}°F\nConditions: {weather["weather"]}\nWind Speed: {weather["wind"]}\nHumidity: {weather["humidity"]}\nPrecipitation: {weather["precipitation"]}"""
        )
        return True
    return False
