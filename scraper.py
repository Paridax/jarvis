from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re


def trim_html(
        text, delete_newlines=False, delete_attributes=None, clear_tags=None, delete_tags=None, remove_repeats=None,
        delete_empty=None, delete_links=True, delete_images=True
):
    # use regex to delete style and javascript. /<script[\s\S]*<\/script>/g and /<style[\s\S]*<\/style>/g
    if delete_empty is None:
        delete_empty = ["div", "span", "p", "li", "ul", "ol"]
    if remove_repeats is None:
        remove_repeats = ["div", "/div", "span", "/span", "p", "/p", "li", "/li", "ul", "/ul", "ol", "/ol"]
    if delete_tags is None:
        delete_tags = ["span", "h1", "h2", "p", "text"]
    if clear_tags is None:
        clear_tags = ["div", "b", "i", "u", "em", "strong", "li", "ul", "ol", "br", "hr", "svg"]
    if delete_attributes is None:
        delete_attributes = ["class", "id", "style", "width", "height", "alt", "aria-label", "data-lams", "data-metric",
                             "data-url", "jscontroller", "jsaction", "jsname", "jslog", "data-ved",
                             "data", "ping"]
    if delete_links:
        delete_attributes.append("href")
    if delete_images:
        delete_attributes.append("src")
        delete_tags.append("img")
        delete_tags.append("svg")

    text = re.sub(r'''(<(script|style)[^>]*>)([\s\S]*?)(<\/\2>)''', "", text)

    for attribute in delete_attributes:
        # delete all the attributes like class="foo" or id="bar"
        if attribute == "data":
            text = re.sub(fr'''({attribute}-[^=]*="[^"]*")''', "", text)
        else:
            text = re.sub(fr'''({attribute}="[^"]*")''', "", text)
    for tag in clear_tags:
        # delete all data from the tags like <div aria-label="foo">bar</div> to <div>bar</div>
        text = re.sub(fr'''(<{tag}[^>]*?)(.*?>)''', f"<{tag}>", text)
    for tag in delete_tags:
        # delete all the tags like <span>foo</span> to foo
        text = re.sub(fr'''(</?{tag}[^>]*?>)''', " ", text)
    for tag in remove_repeats:
        # remove any repeats of the same tag like <div><div>foo</div></div> to <div>foo</div>
        text = re.sub(fr'''<{tag}[^>]*>(\s*<{tag}[^>]*>)*\s*''', f"<{tag}>", text)
    for tag in delete_empty:
        # delete any empty tags like <div></div> to ""
        text = re.sub(fr'''<div>\s*[\n\r\s]*\s*</div>''', "", text)

    # convert any spaces larger than 3 to 3
    text = re.sub(r'''( {2,})''', " ", text)

    if delete_newlines:
        # convert any newlines to spaces
        text = re.sub(r'''([\n\r])''', " ", text)
    return text


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)


def weather(region_name):
    global driver
    search_query = f"weather {region_name}"
    search_query = search_query.replace(" ", "%20")
    driver.get(f"https://www.google.com/search?q={search_query}")
    elem = driver.find_element(By.ID, "rcnt")

    temperature_f = driver.find_element(By.ID, "wob_tm")

    location = driver.find_element(By.ID, "wob_loc")
    time = driver.find_element(By.ID, "wob_dts")
    weather = driver.find_element(By.ID, "wob_dc")

    precipitation = driver.find_element(By.ID, "wob_pp")
    humidity = driver.find_element(By.ID, "wob_hm")
    wind_mph = driver.find_element(By.ID, "wob_ws")

    forecast = driver.find_elements(By.CLASS_NAME, "wob_df")

    daily_forecast = []

    for i in range(len(forecast)):
        day = forecast[i].find_element(By.CLASS_NAME, "Z1VzSb").get_attribute("aria-label")
        day_weather = forecast[i].find_element(By.CLASS_NAME, "uW5pk").get_attribute("alt")
        high = forecast[i].find_elements(By.CLASS_NAME, "wob_t")[0]
        low = forecast[i].find_elements(By.CLASS_NAME, "wob_t")[-2]

        daily_forecast.append({
            "day": day,
            "weather": day_weather,
            "high": high.text,
            "low": low.text,
        })

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


def search(query, single_result=False, two_results=False):
    global driver

    search_query = query.strip().replace(" ", "%20")
    driver.get(f"https://www.google.com/search?q={search_query}")
    elem = driver.find_element(By.ID, "rcnt")
    all_results = elem.find_elements(By.CLASS_NAME, "MjjYud")

    top_tile = None
    try:
        top_tile = driver.find_element(By.ID, "Odp5De")
    except Exception as e:
        pass
    if top_tile:
        # add to beginning of list
        all_results.insert(0, top_tile)

    if single_result:
        return f'''<div>{trim_html(all_results[0].get_attribute("innerHTML"), delete_newlines=True, delete_images=True, delete_links=True)}</div>'''
    elif two_results:
        try:
            return f'''<div>{trim_html(all_results[0].get_attribute("innerHTML"), delete_newlines=True, delete_images=True, delete_links=True)}</div> <div>{trim_html(all_results[1].get_attribute("innerHTML"), delete_newlines=True)}</div>'''
        except Exception as e:
            try:
                return f'''<div>{trim_html(all_results[0].get_attribute("innerHTML"), delete_newlines=True, delete_images=True, delete_links=True)}</div>'''
            except Exception as e:
                return ""
    else:
        results = []
        for i in range(len(all_results)):
            print(trim_html(f'''{i + 1}. {all_results[i].get_attribute("innerHTML")}''', delete_newlines=True,
                            delete_images=True, delete_links=True))
        return all_results

# print(weather("amsterdam"))
#
# while True:
#     query = input("Search: ")
#     if query.strip() == "":
#         break
#     print(search(query, two_results=True))
#
# driver.close()
