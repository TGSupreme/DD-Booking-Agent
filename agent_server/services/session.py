from tools.login import login

access_token = (login({
    "email": "user@gmail.com",
    "password": "123456"
}))['token']

sessions = {}
MAX_TURNS = 10


def default_state():
    return {
        # trip info
        "from_city": None,
        "to_city": None,
        "date": None,
        "passengers": 1,

        # selection
        "selected_bus": None,
        "selected_trip": None,
        "selected_seat": [],
        "base_price": None,

        # workflow flags
        "ticket_id": None,
        "booking_confirmed": False,

        #authorization
        "is_logged_in" : True,
        "access_token" : access_token
    }

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "state": default_state(),
            "access_token": access_token
        }
    return sessions[session_id]


def add_to_history(session, role, content):
    session["history"].append({
        "role": role,
        "content": content
    })

    # trim automatically
    session["history"] = session["history"][-MAX_TURNS*2:]

def print_history(session, limit=None):
    """
    Pretty-print conversation history.

    Args:
        session (dict): session object from get_session()
        limit (int | None): show only last N messages (default: all)
    """
    history = session.get("history", [])

    if not history:
        print("No conversation history.")
        return

    if limit:
        history = history[-limit:]

    print("\n=== Conversation History ===\n")

    for i, msg in enumerate(history, 1):
        role = msg["role"].upper()
        content = msg["content"]

        print(f"{i:02d}. [{role}]")
        print(f"    {content}\n")

    print("============================\n")
    
def set_state_findBus(state: dict, payload: dict) -> None:
    required = ["from", "to"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise ValueError(f"Missing fields: {missing}")

    
    state.update({
    "from_city": payload["from"],
    "to_city": payload["to"],
    })

    if "traveldate" in payload:
        state["date"] = payload["traveldate"]

def set_token(session, token):
    state = session.get('state')
    state.update({
        "is_logged_in" : True,
        "access_token": token,
    })
