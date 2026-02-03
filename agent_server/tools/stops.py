from .base import get

def get_all_stops():
    data = get("/admin/route/stops")
    stops = data["allstops"]
    return stops
