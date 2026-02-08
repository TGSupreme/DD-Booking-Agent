import requests
from config import BASE_URL


# def search_bus(payload: dict):

#     if(payload['traveldate'] !=  None):
#         # print(payload)
#         return requests.post(
#             f"{BASE_URL}/user/search",
#             json=payload
#         ).json()
#     else:
#         del payload['traveldate']
#         return requests.post(
#             f"{BASE_URL}/ai/getbus",
#             json=payload
#         ).json()


from langchain_core.tools import tool


@tool
def search_bus(from_city: str, to_city: str, date: str | None):
    """
    This is the ONLY tool allowed for bus-related queries.

    Purpose:
    - Fetch real bus availability between two cities.

    Parameters:
    - from_city (str): Source city name
    - to_city (str): Destination city name
    - date (str | None):
        • Format: YYYY-MM-DD (ISO 8601), e.g., 2026-01-24
        • If provided → returns buses for that specific date only
        • If None → returns all buses on the route (no date filtering)

    Behavior:
    - With date  → POST /user/search   { from, to, traveldate }
    - Without date → POST /ai/getbus   { from, to }

    STRICT RULES:
    - Always use this tool for bus queries.
    - Do not manually answer.
    - Do not use any other tools.
    """

    payload = {
        "from": from_city,
        "to": to_city,
        "traveldate": date
    }
    print(f"payload by llm : {payload}")
    if(date !=  None):
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

