# from .base import post

# def create_ticket(payload):
#     return post("/ticket/", payload)

from typing import List
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from .base import post
from langchain_core.runnables import RunnableConfig
import json

# ---------- Passenger schema ----------
class Passenger(BaseModel):
    name: str = Field(..., description="Passenger full name")
    age: int = Field(..., description="Passenger age")
    gender: str = Field(..., description="Passenger gender: male/female/other")


# ---------- Input schema ----------
class CreateTicketInput(BaseModel):
    tripId: str = Field(..., description="Trip ID of selected bus")
    from_city: str = Field(..., description="Source city name")
    to_city: str = Field(..., description="Destination city name")
    price: float = Field(..., description="Total ticket price")
    seats: List[int] = Field(..., description="List of seat numbers selected")
    passengers: List[Passenger] = Field(..., description="Passenger details. Count MUST equal number of seats exactly.")
    ticketdate: str = Field(..., description="Travel date in YYYY-MM-DD format")


# ---------- Core function ----------
def _create_ticket(
    tripId: str,
    from_city: str,
    to_city: str,
    price: float,
    seats: List[int],
    passengers: List[Passenger],
    ticketdate: str,
    config: RunnableConfig,
):

    print(f"Calling create ticket Tool")
    token = config["configurable"]["session"]['access_token']

    if len(seats) != len(passengers):
        return (
            f"Seats count ({len(seats)}) must equal passengers count ({len(passengers)}). "
            "Collect all passenger details first."
        )

    payload = {
        "tripId": tripId,
        "from": from_city,
        "to": to_city,
        "price": price,
        "seats": seats,
        "passengers": [p.dict() for p in passengers],
        "ticketdate": ticketdate,
    }
    print(f"payload by llm : {payload}")


    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = post("/ticket/", payload, headers=headers)

    if not res.get("success"):
        raise RuntimeError(res.get("message", "Ticket creation failed"))

    return json.dumps(res.get("ticket"))
    

# ---------- Tool ----------
create_ticket_tool = StructuredTool.from_function(
    func=_create_ticket,
    name="create_ticket",
    description=(
        "Create a ticket booking for the selected trip. "
        "Call this ONLY AFTER seats have been selected and passenger details have been collected. "
        "Do NOT call get_all_seats again once seats are chosen. "
        "You MUST collect passenger details for EVERY seat. "
        "The number of passengers MUST EXACTLY match the number of seats selected. "
        "If seats = 2, the passengers list MUST contain exactly 2 passenger objects. "
        "Never drop, merge, or auto-fill passengers. "
        "Requires: seats list and passenger details. "
        "Returns the booked ticket confirmation as a JSON string."
    ),
    args_schema=CreateTicketInput,
)