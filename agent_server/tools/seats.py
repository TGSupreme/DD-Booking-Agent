from typing import List
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from .base import post
from langchain_core.runnables import RunnableConfig


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
    token = config["configurable"]["session"]['access_token']
    payload = {
        "tripId": tripId,
        "from": from_city,
        "to": to_city,
        "traveldate": traveldate,
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = post("/ticket/seat/get", payload, headers=headers)

    if not res.get("success"):
        raise RuntimeError(res.get("message", "Seat fetch failed"))

    return res.get("bookedseat", [])


# ---------- Tool ----------
get_all_seats_tool = StructuredTool.from_function(
    func=_get_all_seats,
    name="get_all_seats",
    description=(
        "Fetch all already booked seat numbers for a bus trip. "
        "Call this before seat selection. "
        "Returns list of booked seat numbers."
    ),
    args_schema=GetAllSeatsInput,
)
