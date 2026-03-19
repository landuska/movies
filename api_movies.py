import requests
import os
from dotenv import load_dotenv
import re

load_dotenv(dotenv_path="config/.env")
API_KEY = os.getenv('API_KEY')


def normalize(text):
    return re.sub(r"[^a-zA-Z0-9]", " ", text)


def get_movie(t: str):
    """Send a request to get a movie from the API."""

    url_api = "https://www.omdbapi.com"

    params = {
        "apikey": API_KEY,
        "t": t,
    }

    try:
        response = requests.get(url_api, params=params)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

    data = response.json()
    print(data["Response"])
    if data["Response"] == "False":
        print(f"Movie '{t}' not found")
        return []

    title = normalize(data.get("Title", "Unknown Title"))
    year = normalize(data.get("Year", "Unknown Year"))
    rating = data.get("imdbRating", None)
    image = data.get("Poster", None)

    return title, year, rating, image
