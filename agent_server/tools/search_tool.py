from langchain.tools import tool
from .search_bus import search_bus

@tool
def search_bus_tool(from_: str, to: str, traveldate: str):
    """
    Search available buses between two cities for a given date.
    """
    payload = {
        "from": from_,
        "to": to,
        "traveldate": traveldate
    }

    return search_bus(payload)