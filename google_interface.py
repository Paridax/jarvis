from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re


class Google:
    def __init__(self, headless=True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def weather(self, region_name):
        """
        Get the weather for a given region.
        :param str region_name:
        :return data: a dictionary containing the weather data
        """
        # open a new search
        search_query = f"weather {region_name}"
        search_query = search_query.replace(" ", "%20")
        self.driver.get(f"https://www.google.com/search?q={search_query}")

        temperature_f = self.driver.find_element(By.ID, "wob_tm")
        location = self.driver.find_element(By.ID, "wob_loc")
        time = self.driver.find_element(By.ID, "wob_dts")
        weather = self.driver.find_element(By.ID, "wob_dc")
        precipitation = self.driver.find_element(By.ID, "wob_pp")
        humidity = self.driver.find_element(By.ID, "wob_hm")
        wind_mph = self.driver.find_element(By.ID, "wob_ws")
        forecast = self.driver.find_elements(By.CLASS_NAME, "wob_df")

        daily_forecast = []

        for i in range(len(forecast)):
            day = (
                forecast[i]
                .find_element(By.CLASS_NAME, "Z1VzSb")
                .get_attribute("aria-label")
            )
            day_weather = (
                forecast[i].find_element(By.CLASS_NAME, "uW5pk").get_attribute("alt")
            )
            high = forecast[i].find_elements(By.CLASS_NAME, "wob_t")[0]
            low = forecast[i].find_elements(By.CLASS_NAME, "wob_t")[-2]

            daily_forecast.append(
                {
                    "day": day,
                    "weather": day_weather,
                    "high": high.text,
                    "low": low.text,
                }
            )

        data = {
            "temp": temperature_f.text,
            "wind": wind_mph.text,
            "location": location.text,
            "time": time.text,
            "weather": weather.text,
            "precipitation": precipitation.text,
            "humidity": humidity.text,
            "forecast": daily_forecast,
        }

        return data

    def search(self, query, text=False, links=None):
        """
        Search for a query on Google.
        :param links:
        :param text:
        :param query:
        :return:
        """

        textData = None
        linkData = None

        # remove unnecessary spaces
        query = query.strip().replace(" ", "%20")

        # open a new search
        self.driver.get(f"https://www.google.com/search?q={query}")

        # get the search results
        results = self.driver.find_element(By.ID, "rcnt")
        # try to delete div with id of "taw", which is spellcheck
        try:
            self.driver.execute_script("document.getElementById(\"taw\").remove()")
        except Exception as e:
            pass

        if text:
            # remove all newlines and replace with semicolons
            cleaned = results.text.replace("\n", "  ")
            # use regex to remove all extra spaces and replace with a single space
            cleaned = re.sub(" +", " ", cleaned)

            textData = cleaned

        if links is not None:
            # get all anchors
            anchors = results.find_elements(By.TAG_NAME, "a")

            verified_links = []

            for anchor in anchors:
                try:
                    link = anchor.get_attribute("href")
                    verified_links.append(
                        {
                            "text": anchor.text.replace("\n", " "),
                            "link": link,
                        }
                    )
                    if link.startswith("http"):
                        pass
                except Exception as e:
                    pass
            # trim the list to the number of links wanted
            if len(verified_links) > links:
                verified_links = verified_links[:links]

            linkData = verified_links

        if text and not links:
            return textData
        elif links and not text:
            return linkData
        elif text and links:
            # join the results into a single string
            return (
                textData
                + "\nPAGE LINKS: "
                + "\n".join([f"{link['text']}: {link['link']}" for link in linkData])
            )

        verified_results = []

        for result in results.find_elements(By.CLASS_NAME, "MjjYud"):
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = result.find_element(
                    By.XPATH, ".//div/div/div[2]/div"
                ).text

                # print("title)
                # print(link)
                # print(description)
                # print("", end="")

                verified_results.append(
                    {
                        "title": title,
                        "link": link,
                        "description": description,
                    }
                )
            except Exception as e:
                pass

        # print(verified_results)

        return verified_results


if __name__ == "__main__":
    g = Google()
    # weather = g.weather("New York")
    # print(weather)
    print(g.search("joe biden age", text=True, links=5))
