from .base import get

def get_all_stops():
    return get("/admin/route/stops")
