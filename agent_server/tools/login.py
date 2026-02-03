from .base import post

def login(payload):
    return post("/login", payload)