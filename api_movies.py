import requests
import os
from dotenv import load_dotenv
import re

load_dotenv(dotenv_path="config/.env")
API_KEY = os.getenv('API_KEY')


def normalize(text):
    """
        Removes special characters from a string, keeping only alphanumeric characters and spaces.

    Args:
        text (str): The string to be normalized.

    Returns:
        str: The cleaned string with special characters replaced by spaces.
    """
    return re.sub(r"[^a-zA-Z0-9]", " ", text)


def get_movie(t: str):
    """
    Fetches movie details from the OMDb API based on a title.

    Args:
        t (str): The title of the movie to search for.

    Returns:
        tuple: A tuple containing (title, year, rating, image) if found.
        list: An empty list if the movie is not found or a network error occurs.
    """

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
