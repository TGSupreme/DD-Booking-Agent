import requests
from config import BASE_URL


def search_bus(payload: dict):

    return requests.post(
        f"{BASE_URL}/user/search",
        json=payload
    ).json()
