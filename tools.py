from datetime import datetime
import requests
from ddgs import DDGS


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    return response.text

def duckduckgo_search(query, max_results=5):
      """Search the web using DuckDuckGo."""
      results = DDGS().text(
          query,
          max_results=max_results,
          backend="duckduckgo"
      )
  
      return [
          {
              "title": result.get("title", ""),
              "url": result.get("href", ""),
              "snippet": result.get("body", "")
          }
          for result in results
      ]

TOOLS = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_current_time",
            "description" : "Returns the current date and time in formated strings.",
            "parameters" : {
                "type" : "object",
                "properties" : {}
            }
        }

    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_city_weather",
            "description" : "return the current weather of the city.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "City to get the weather for",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "duckduckgo_search",
            "description": (
                "Searches the web using DuckDuckGo and returns "
                "titles, URLs, and snippets of relevant results."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return.",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"]
            }
        }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "duckduckgo_search": duckduckgo_search

}