from services.intent_extractor import extract_intent
from tools.search_bus import search_bus
from agent.formatter import format_bus_list
from agent.intent_router import route_intent


FALLBACK_MSG = "This service is not available yet."


# def handle_message(message: str) -> str:
#     parsed = extract_intent(message)

#     intent = parsed.get("intent")
#     params = parsed.get("parameters", {})

#     if intent == "search_bus":
#         api_response = search_bus(params)

#         # convert JSON → text here
#         return format_bus_list(api_response)

#     return "This service is not available yet."

def handle_message(message: str) -> str:
    intent = route_intent(message)

    print(type(intent))

    if((intent["intent"] == "conversational") or (intent["intent"] == "unrelated")):
        return (intent['response'])
    
    if((intent["intent"] == "action")):
        return "you are in the action case"
    
    if((intent["intent"] == "action")):
        return "you are in the action case"
    return intent

