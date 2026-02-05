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

        # workflow flags
        "booking_confirmed": False
    }

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "state": default_state(),
            "access_token": None
        }
    return sessions[session_id]


def add_to_history(session, role, content):
    session["history"].append({
        "role": role,
        "content": content
    })

    # trim automatically
    session["history"] = session["history"][-MAX_TURNS*2:]
    