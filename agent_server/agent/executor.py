from agent.action_router import route_action
from agent.intent_router import route_intent
from services.session import add_to_history, print_history
from agent.handler.handle_conversation import handle_conversation

FALLBACK_MSG = "This service is not available yet."


#this function is the entry point to our agentic system
#it decide what query's type is and which agent will execute it  
def handle_message(message: str, session) -> str:
    reply = None
    

    intent = route_intent(message , session)
    intent_name = intent["intent"]

    print(f"Intent provided by Intent-Router : {intent.get('intent', 'UNKNOWN')}")

    
    if (intent_name == "unsupported"):
        reply = "This action is not supported yet."

    elif intent_name == "unrelated":
        reply = "I can only help with bus booking and ticket related requests."

    elif intent_name == "conversational":
        reply = handle_conversation(message , session)
    
    elif intent_name == "action":
        reply = route_action(message, session)

    

    if reply is None:
        print ("intent doesnt match any case (intent_router failed)")
        return "Your query is soo amazing our server exploded congrats......"
    else:
        add_to_history(session, "user", message)
        add_to_history(session, "assistant", reply)
        # print_history(session)
        return reply
