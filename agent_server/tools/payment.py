from .base import put

def complete_ticket_payment(ticket_id, payload):
    return put(f"/ticket/update/payment/{ticket_id}", payload)
