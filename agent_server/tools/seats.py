from .base import post

def get_all_seats(payload):
    return post("/ticket/seat/get", payload)
