import requests
from config import BASE_URL

def post(path, payload=None, headers=None):
    res = requests.post(BASE_URL + path, json=payload, headers=headers)
    return res.json()


def get(path, headers=None):
    res = requests.get(BASE_URL + path, headers=headers)
    return res.json()


def put(path, payload=None, headers=None):
    res = requests.put(BASE_URL + path, json=payload, headers=headers)
    return res.json()