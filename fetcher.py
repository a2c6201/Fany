import requests

import config

HOT_PEPPER_API_KEY = config.HOT_PEPPER_API_KEY

HOT_PEPPER_API_URL = config.HOT_PEPPER_API_URL
GOOGLE_MAPS_API_URL = config.GOOGLE_MAPS_API_URL


def search(query):
    responce = requests.get(HOT_PEPPER_API_URL, query)
    return responce
