from typing import List
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from .base import post
from langchain_core.runnables import RunnableConfig
import json
import time

# ---------- Input schema ----------
class GetAllSeatsInput(BaseModel):
    tripId: str = Field(..., description="Unique trip ID of the selected bus")
    from_city: str = Field(..., description="Source city name")
    to_city: str = Field(..., description="Destination city name")
    traveldate: str = Field(..., description="Travel date in YYYY-MM-DD format")


# ---------- Core function ----------
def _get_all_seats(
    tripId: str,
    from_city: str,
    to_city: str,
    traveldate: str,
    config: RunnableConfig,
) -> List[int]:
    
    tool_start = time.perf_counter()
    print("[get_all_seats] start")

    print(f"Calling seats Tool")
    
    t0 = time.perf_counter()

    session = config["configurable"]["session"]
    token = session['access_token']
    state = session['state']
    state['selected_trip'] = tripId


    payload = {
        "tripId": tripId,
        "from": from_city,
        "to": to_city,
        "traveldate": traveldate,
    }

    print(f"payload by llm (seats): {payload}")

    headers = {
        "Authorization": f"Bearer {token}"
    }
    print(f"Headers : {headers}")
    t1 = time.perf_counter()
    print(f"[get_all_seats] prep: {t1 - t0:.3f}s")

    api_start = time.perf_counter()

    res = post("/ticket/seat/get", payload, headers=headers)

    api_end = time.perf_counter()
    print(f"[get_all_seats] backend API: {api_end - api_start:.3f}s")

    t2 = time.perf_counter()
    if not res.get("success"):
        raise RuntimeError(res.get("message", "Seat fetch failed"))

    state["booked_seats"] = res.get("bookedseat", [])

    t3 = time.perf_counter()
    print(f"[get_all_seats] post-process: {t3 - t2:.3f}s")

    # -------------------------
    print(f"[get_all_seats] total: {t3 - tool_start:.3f}s")
    
    print(res)
    return  json.dumps(res.get("bookedseat", []))


# ---------- Tool ----------
get_all_seats_tool = StructuredTool.from_function(
    func=_get_all_seats,
    name="get_all_seats",
    description=(
    "Fetch already booked seats for a selected trip. "
    "Call this ONLY once immediately after the user selects a bus. "
    "DO NOT call this after the user has provided seat numbers. "
    "If seat numbers are provided, you MUST use create_ticket instead. "
    "Returns a JSON string list of booked seat numbers. "
    "An empty list means all seats are available."
    ),  
    args_schema=GetAllSeatsInput,
)
