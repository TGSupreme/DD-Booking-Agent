from .base import post

def search_bus(payload):
    return post("/user/search", payload)
