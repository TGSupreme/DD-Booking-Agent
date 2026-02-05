from tools.search_bus import search_bus
from tools.stops import get_all_stops
from services.llm import get_llm
import json
from datetime import date
from services.llm import get_llm
from agent.formatter import format_bus_list
from agent.prompts.prompts import EXTRACT_BUS_PARAMETER_PROMPT

def handle_search_bus(message):
    intent = extract_params(message)
    payload = intent['parameters']
    
    if (intent["intent"] == "invalid_stop"):
        invalid_stop = (intent["parameters"])['invalid_stop']
        return f"{invalid_stop} is not a valid station"
    
    elif (intent["intent"] == "invalid_date"):
        invalid_date = (intent["parameters"])['invalid_date']
        return f"{invalid_date} is not a valid date (are you dumb that why you are single bcz you cannot find a date)"
    
    else:
        print(payload)
        apiResponse =  search_bus(payload)
        return format_bus_list(apiResponse)


def extract_params(message):
    stops = get_all_stops()
    TODAY = date.today().isoformat()
    llm = get_llm()
    
    SYSTEM_PROMPT = EXTRACT_BUS_PARAMETER_PROMPT.format(TODAY = TODAY, stops = json.dumps(stops))

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
    
