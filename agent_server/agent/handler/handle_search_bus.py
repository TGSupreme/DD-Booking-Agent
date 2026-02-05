from tools.search_bus import search_bus
from tools.stops import get_all_stops
import json
from datetime import date
from services.llm import get_llm
from agent.formatter import format_bus_list
from agent.prompts.prompts import EXTRACT_BUS_PARAMETER_PROMPT
from services.session import set_state_findBus

def handle_search_bus(message, session):
    intent = extract_params(message, session)
    intent_name = intent.get("intent")
    print(f"Response provided by extract_params : {intent}")

    payload = intent.get("parameters", {})

    state = session["state"]
    
    if intent_name == "invalid_stop":
        return f"{payload.get('invalid_stop')} is not a valid station"

    if intent_name == "invalid_date":
        return f"{payload.get('invalid_date')} is not a valid date. Please use YYYY-MM-DD."

    
    else:
        # print(f"Payload provided by extract_params : {payload}")


        set_state_findBus(state, payload)
        
        apiResponse =  search_bus(payload)
        return format_bus_list(apiResponse)


def extract_params(message, session):
    stops = get_all_stops()
    TODAY = date.today().isoformat()
    llm = get_llm()
    
    SYSTEM_PROMPT = EXTRACT_BUS_PARAMETER_PROMPT.format(TODAY = TODAY, 
                                                        stops = json.dumps(stops),
                                                        history= session['history'],
                                                        state= session['state'])

    
    prompt = [
        ("system", SYSTEM_PROMPT),
        ("user", message)
    ]

    response = llm.invoke(prompt)
    
    try:
        intent = json.loads(response.content.strip())
        return intent

    except json.JSONDecodeError:
        raise ValueError(f"LLM returned invalid JSON: {response.content}")
    
