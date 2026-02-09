# from .base import put

# def complete_ticket_payment(ticket_id, payload):
#     return put(f"/ticket/update/payment/{ticket_id}", payload)

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Dict, Any
from .base import put


# ---------- Input schema ----------
class CompleteTicketPaymentInput(BaseModel):
    ticketId: str = Field(..., description="Ticket ID returned from create_ticket API")
    price: float = Field(..., description="Total amount paid for the ticket")


# ---------- Core function ----------
def _complete_ticket_payment(
    ticketId: str,
    price: float,
) -> Dict[str, Any]:

    payload = {
        "price": price
    }

    res = put(f"/ticket/update/payment/{ticketId}", payload)

    if not res.get("success"):
        raise RuntimeError(res.get("message", "Payment update failed"))

    return res.get("updatedTicket")


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
