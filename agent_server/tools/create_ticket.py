# from .base import post

# def create_ticket(payload):
#     return post("/ticket/", payload)

from typing import List
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from .base import post


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
    passengers: List[Passenger] = Field(..., description="Passenger details list")
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
):

    payload = {
        "tripId": tripId,
        "from": from_city,
        "to": to_city,
        "price": price,
        "seats": seats,
        "passengers": [p.dict() for p in passengers],
        "ticketdate": ticketdate,
    }

    res = post("/ticket/", payload)

    if not res.get("success"):
        raise RuntimeError(res.get("message", "Ticket creation failed"))

    return res.get("ticket")
    

# ---------- Tool ----------
create_ticket_tool = StructuredTool.from_function(
    func=_create_ticket,
    name="create_ticket",
    description=(
        "Create a new ticket booking for a selected trip. "
        "Requires trip info, seat numbers, passenger details, and price. "
        "Returns the booked ticket object including PNR."
    ),
    args_schema=CreateTicketInput,
)