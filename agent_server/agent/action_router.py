from services.llm import get_llm
import json
from agent.handler.handle_search_bus import handle_search_bus
from agent.prompts.prompts import ACTION_ROUTER_PROMPT

llm = get_llm()

def route_action(message: str):
    
    prompt = [
    ("system", ACTION_ROUTER_PROMPT),
    ("user", message)
    ]
    
    response = llm.invoke(prompt)
    content = json.loads(response.content)

    if (content['intent'] == 'search_bus'):
        return handle_search_bus(message)
    
    print(content)

    return (f"message came in action router {message}")
