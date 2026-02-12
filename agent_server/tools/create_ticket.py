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
    state = config["configurable"]["session"]['state']

    if len(seats) != len(passengers):
        raise ValueError("PASSENGER_COUNT_MISMATCH")

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

    state["create_ticket_response"] = res

    if not res.get("success"):
        raise RuntimeError(res.get("message", "Ticket creation failed"))

    return json.dumps(res.get("ticket"))
    

# ---------- Tool ----------
create_ticket_tool = StructuredTool.from_function(
    func=_create_ticket,
    name="create_ticket",
    description=(
    "Creates a ticket. "
    "Return ONLY valid JSON arguments. "
    "Do NOT add explanations or extra fields. "
    "Arguments must exactly match schema. "
    "passengers length MUST equal seats length."
),
    args_schema=CreateTicketInput,
)