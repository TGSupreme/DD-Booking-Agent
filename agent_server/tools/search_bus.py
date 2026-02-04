import requests
from config import BASE_URL


def search_bus(payload: dict):

    if(payload['traveldate'] !=  None):
        print(payload)
        return requests.post(
            f"{BASE_URL}/user/search",
            json=payload
        ).json()
    else:
        del payload['traveldate']
        return requests.post(
            f"{BASE_URL}/ai/getbus",
            json=payload
        ).json()
