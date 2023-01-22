# from googlesearch import search
# import packages for get and post requests
from requests import get
import os
import dotenv

dotenv.load_dotenv()

search_api_key = os.getenv("SEARCH_API_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")


def search(query):
    get_url = f"https://www.googleapis.com/customsearch/v1?key={search_api_key}&cx={search_engine_id}&lr=en&num=5&q={query}"
    result = get(get_url)
    result = result.json()
    try:
        result = result["items"]
        return result
    except Exception as e:
        return result


def get_weather(city, ):


def main():
    # query = "when was the empire state building built"
    # query = "when did queen elizabeth ii die"
    query = "weather in new york"
    query_intent = "local weather"

    if query_intent == "search":
        results = search(query)
    elif query_intent == "weather":


    all_results = ""

    # for result in results:
    #     if "snippet" in result:
    print(results)


if __name__ == "__main__":
    main()