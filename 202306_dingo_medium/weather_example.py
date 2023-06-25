from agent_dingo import AgentDingo
from agent_dingo.context import ChatContext

agent = AgentDingo()
import os

# set the openweathermap api key as an environment variable before running the script
# ATTENTION: after generating the key, it takes several hours until it is activated!
openweathermap_api_key = os.environ.get("OPENWEATHERMAP_API_KEY", None)

if openweathermap_api_key is None:
    print("Using fake weather api.")
    import random

    random.seed(42)

    class response_:
        def json(*args, **kwargs):
            random_temp = random.randint(20, 30)
            feels_like = random_temp + random.randint(-5, 5)
            temp_min = random_temp + random.randint(-5, 0)
            temp_max = random_temp + random.randint(0, 5)
            pressure = random.randint(1000, 1100)
            humidity = random.randint(10, 70)
            return {
                "main": {
                    "temp": random_temp,
                    "feels_like": feels_like,
                    "temp_min": temp_min,
                    "temp_max": temp_max,
                    "pressure": pressure,
                    "humidity": humidity,
                }
            }

    class requests:
        def get(base_url, params, *args, **kwargs):
            return response_()

else:
    import requests


@agent.function
def get_temperature(city: str) -> str:
    """Retrieves the current temperature in a city.

    Parameters
    ----------
    city : str
        The city to get the temperature for.

    Returns
    -------
    float
        str representation of the json response from the weather api.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": openweathermap_api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()
    print("get_temperature function output :", data["main"])
    return str(data)


# Example 1: Single function call
print("\n-----------------------------------\n")
query = "What is the current weather in Linz?"
print("query:", query)
result = agent.chat(query, temperature=0.0)[0]

print(result)

# Example 2: Multiple function calls
print("\n-----------------------------------\n")
query = "Is it warmer in Madrid or Barcelona right now?"
print("query:", query)
result = agent.chat(query, temperature=0.0)[0]
print(result)


# Example 3: Call with the context
@agent.function
def get_user_location(chat_context: ChatContext) -> str:
    print("Requested user location.")
    return chat_context.get("user_location", "The location is unknown.")


print("\n-----------------------------------\n")
query = "What is the weather like right now?"
print("query:", query)
result = agent.chat(
    query, temperature=0.0, chat_context=ChatContext(user_location="Amsterdam")
)[0]
print(result)
