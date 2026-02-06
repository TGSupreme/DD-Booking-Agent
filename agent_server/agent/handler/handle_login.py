
from tools.login import login, validate_credentials
from services.llm import get_llm
import json
from datetime import date
from agent.formatter import format_bus_list
from agent.prompts.prompts import EXTRACT_LOGIN_PARAMETER_PROMPT
from services.session import set_token

def process_login(payload, session):
    validation = validate_credentials(payload)

    if(validation):

        print("Calling LOGIN API.......")
        apiResponse =  login(payload)
            
        if (apiResponse['success'] ):
            set_token(session, apiResponse['token'])
            return (apiResponse)
        else:
            return apiResponse['message']
        
    else:
        return validation   


def handle_login(message, session):

    intent = extract_params(message, session)

    payload = intent.get("parameters", {})
    intent_name = intent.get('intent')

    print(f"Response provided by extract_params(login) : {intent_name , payload.get('message')}")
    

    if intent_name == 'invalid_credentials':
        return payload['message']
    
    elif intent_name == 'login':
        return process_login(payload, session)
    else:
        return "failed to extract parameters please try again"
        
    


def extract_params(message, session):
    llm = get_llm()
    prompt = [
        ("system", EXTRACT_LOGIN_PARAMETER_PROMPT.format(history = session['history'],
                                                         state = session['state'])),
        ("user", message)
    ]

    response = llm.invoke(prompt)
    intent = json.loads(response.content.strip())
    return (intent)