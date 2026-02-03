import requests
from config import BASE_URL

def post(path, payload):
    return requests.post(BASE_URL + path, json=payload).json()

def get(path):
    return requests.get(BASE_URL + path).json()

def put(path, payload):
    return requests.put(BASE_URL + path, json=payload).json()
