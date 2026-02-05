from services.llm import get_llm
import json
from agent.action_router import route_action
from agent.prompts.prompts import INTENT_PROMPT


llm = get_llm()

def route_intent(message: str, session):
    
    prompt = [
    ("system", INTENT_PROMPT),
    ("user", message)
    ]
    
    response = llm.invoke(prompt)
    content = json.loads(response.content)

    # print(content)

    return content
