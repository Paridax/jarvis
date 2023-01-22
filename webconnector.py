from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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


def main():
    driver = webdriver.Chrome()

    search_query = "weather"

    # percent encode the search query
    search_query = search_query.replace(" ", "%20")

    driver.get(f"https://www.google.com/search?q={search_query}")
    # get element with id "rcnt"
    # rcnt is the element that contains the search results, but not the search bar
    elem = driver.find_element(By.ID, "rcnt")

    # rhs is the tile to the right of the search results, which sometimes has relevant information
    data_tile = None
    try:
        data_tile = driver.find_element(By.ID, "rhs")
        print("Data tile: " + f'''<div>{trim_html(data_tile.get_attribute("innerHTML"), delete_newlines=True)}</div>''')
    except Exception as e:
        print("No data tile found")
        pass

    search_results = elem.find_elements(By.CLASS_NAME, "MjjYud")

    for i in range(len(search_results)):
        print(f"Search elem {i}: " + f'''<div>{trim_html(search_results[i].get_attribute("innerHTML"), delete_newlines=True)}</div>''')

    driver.close()


def weather(region_name):
    driver = webdriver.Chrome()

    search_query = f"weather {region_name}"
    search_query = search_query.replace(" ", "%20")
    driver.get(f"https://www.google.com/search?q={search_query}")
    elem = driver.find_element(By.ID, "rcnt")

    search_results = elem.find_elements(By.CLASS_NAME, "MjjYud")

    weather = trim_html(search_results[0].get_attribute("innerHTML"), delete_newlines=True)
    driver.close()
    return weather


print(weather("Sydney NSW, Australia"))