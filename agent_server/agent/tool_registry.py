from tools.login import login
from tools.stops import get_all_stops
from tools.search_bus import search_bus
from tools.seats import get_all_seats
from tools.create_ticket import create_ticket
from tools.payment import complete_ticket_payment

TOOLS = {
    "login": login,
    "get_all_stops": get_all_stops,
    "search_bus": search_bus,
    "get_all_seats": get_all_seats,
    "create_ticket": create_ticket,
    "complete_ticket_payment": complete_ticket_payment
}
