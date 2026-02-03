from services.intent_extractor import extract_intent
from tools.search_bus import search_bus
from agent.formatter import format_bus_list


FALLBACK_MSG = "This service is not available yet."


def handle_message(message: str) -> str:
    parsed = extract_intent(message)

    intent = parsed.get("intent")
    params = parsed.get("parameters", {})

    if intent == "search_bus":
        api_response = search_bus(params)

        # convert JSON → text here
        return format_bus_list(api_response)

    return "This service is not available yet."

