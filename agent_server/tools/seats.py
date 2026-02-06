from .base import post


def get_all_seats(payload, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return post("/ticket/seat/get", payload, headers=headers)