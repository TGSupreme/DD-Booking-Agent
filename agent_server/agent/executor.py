from agent.action_router import route_action
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

    print((intent))

    if intent["intent"] in {"conversational", "unrelated", "unsupported"}:
        return intent["response"]
    
    if((intent["intent"] == "action")):
        return route_action(message)
    

    return "intent doesnt match any case (intent_router failed)"

