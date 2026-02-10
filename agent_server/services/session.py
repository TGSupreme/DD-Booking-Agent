from tools.login import login
from agent.prompts.prompts import STATE_EXTRACT_PROMPT
import json
from datetime import date

access_token = (login({
    "email": "user@gmail.com",
    "password": "123456"
}))['token']

sessions = {}
MAX_TURNS = 10


def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "history": [],
            "state": default_state(),
            "access_token": access_token
        }
    return sessions[session_id]

def default_state():
    return {
        "today's_date" : str(date.today()),
        "today_day": date.today().strftime("%A"), 
        # trip info
        "from_city": None,
        "to_city": None,
        "travel_date": None,
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

        "tool_data": {
            "search_bus": None,
            "seat_map": None,
            "price_breakdown": None
        }
    }

def add_to_history(session, role, content):

    session["history"].append({
        "role": role,
        "content": content
    })

    # trim automatically
    session["history"] = session["history"][-MAX_TURNS*2:]

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

def extract_state_from_text(llm, history):

    prompt = STATE_EXTRACT_PROMPT.format(history=history)

    resp = llm.invoke(prompt).content

    try:
        return json.loads(resp)
    except:
        return {}
    
def update_state_from_llm(session, llm):


    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in session["history"]
    )

    extracted = extract_state_from_text(llm, history_text)

    print(f"Extracted Params by LLM : {extracted}")
    state = session["state"]

    for k, v in extracted.items():
        if v is not None:
            state[k] = v

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
    
def print_state(state: dict):
    print(json.dumps(state, indent=2))