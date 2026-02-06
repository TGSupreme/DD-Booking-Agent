from services.llm import get_llm
import json
from agent.action_router import route_action
from agent.prompts.prompts import INTENT_ROUTER_PROMPT


llm = get_llm()

#this function takes user query and return the intent as "conversational | action | unsupported | unrelated "
def route_intent(message: str, session):
    
    prompt = [
    ("system", INTENT_ROUTER_PROMPT),
    ("user", message)
    ]
    
    response = llm.invoke(prompt)
    content = json.loads(response.content)

    # print(content)

    return content
