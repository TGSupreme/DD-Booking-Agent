from .base import post

def create_ticket(payload):
    return post("/ticket/", payload)
