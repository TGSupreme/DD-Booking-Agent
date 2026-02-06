from agent.action_router import route_action
from agent.intent_router import route_intent
from services.session import add_to_history, print_history
FALLBACK_MSG = "This service is not available yet."



def handle_message(message: str, session) -> str:
    reply = None
    

    intent = route_intent(message , session)
    

    print(f"Intent provided by Intent-Router : {intent.get('intent', 'UNKNOWN')}")

    
    if intent["intent"] in {"conversational", "unrelated", "unsupported"}:
        reply = intent["response"]
    
    elif((intent["intent"] == "action")):
        reply = route_action(message, session)
    

    if reply is None:
        print ("intent doesnt match any case (intent_router failed)")
        return "Your query is soo amazing our server exploded congrats......"
    else:
        add_to_history(session, "user", message)
        add_to_history(session, "assistant", reply)
        # print_history(session)
        return reply
