from services.llm import get_llm
import json
from agent.handler.handle_search_bus import handle_search_bus
from agent.handler.handle_login import handle_login
from agent.prompts.prompts import ACTION_ROUTER_PROMPT

llm = get_llm()

def route_action(message: str, session):
    
    prompt = [
    ("system", ACTION_ROUTER_PROMPT),
    ("user", message)
    ]
    
    response = llm.invoke(prompt)
    content = json.loads(response.content)
    intent_name = content['intent']
    
    print(f"Intent provided by Action-Router : {content.get('intent', 'UNKNOWN')}")
    
    if (intent_name == 'search_bus'):
        return handle_search_bus(message, session)
    

    elif (intent_name == 'login'):
        return handle_login(message,session)

    else:
        return (f"message came in action router but this intent is not handles in action_router :  msg{message}")
    
