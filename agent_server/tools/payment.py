from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Dict, Any
from .base import put
from langchain_core.runnables import RunnableConfig
import json

# ---------- Input schema ----------
class CompleteTicketPaymentInput(BaseModel):
    ticketId: str = Field(..., description="Ticket ID returned from create_ticket API")
    price: float = Field(..., description="Total amount paid for the ticket")


# ---------- Core function ----------
def _complete_ticket_payment(
    ticketId: str,
    price: float,
    config: RunnableConfig,
) -> Dict[str, Any]:

    session = config["configurable"]["session"]
    token = session['access_token']

    payload = {
        "price": price
    }
    print(f"Calling seats Tool")
    print(f"payload by llm (Payment): {payload}")


    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = put(f"/ticket/update/payment/{ticketId}", payload, headers=headers)

    if not res.get("success"):
        raise RuntimeError(res.get("message", "Payment update failed"))

    return json.dumps(res.get("updatedTicket"))


# ---------- Tool ----------
complete_ticket_payment_tool = StructuredTool.from_function(
    func=_complete_ticket_payment,
    name="complete_ticket_payment",
    description=(
        "Mark a ticket payment as completed after successful payment. "
        "Use ONLY after ticket is created and payment succeeds. "
        "Returns the updated ticket object with paymentstatus=completed."
    ),
    args_schema=CompleteTicketPaymentInput,
)
