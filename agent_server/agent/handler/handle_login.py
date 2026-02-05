
from tools.login import login
from services.llm import get_llm
import json
from datetime import date
from agent.formatter import format_bus_list
from agent.prompts.prompts import EXTRACT_LOGIN_PARAMETER_PROMPT


def handle_login(message):
    intent = extract_params(message)
    print(intent)
    
    # if intent
    
    # payload = intent['parameters']
    return "lalalalalalala"


def extract_params(message):
    llm = get_llm()
    
    prompt = [
        ("system", EXTRACT_LOGIN_PARAMETER_PROMPT),
        ("user", message)
    ]

    response = llm.invoke(prompt)

    return response