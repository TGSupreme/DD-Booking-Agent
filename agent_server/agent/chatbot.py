from services.llm import get_llm
from services.session import add_to_history
from agent.prompts.prompts import CONVERSATION_AGENT_PROMPT

llm = get_llm()


def conversation(user_message, session):
    
    prompt = [
    ("system", CONVERSATION_AGENT_PROMPT.format(history = session.get('history'),
                                                state = session.get('state'))),
    ("user", user_message)
    ]
    response = llm.invoke(prompt)
    
    return response