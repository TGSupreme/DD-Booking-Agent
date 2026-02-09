import requests
from config import BASE_URL
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from services.session import set_state_findBus 
from tools.tool_descriptions import SEARCH_BUS_DOCSTRING

def search_bus_api_call(payload, session):
    apiResponse = None
    print(f"payload by llm : {payload}")

    if(payload['traveldate'] !=  None):
        apiResponse =  requests.post(
            f"{BASE_URL}/user/search",
            json=payload
        ).json()
    
    else:
        del payload['traveldate']
        apiResponse = requests.post(
            f"{BASE_URL}/ai/getbus",
            json=payload
        ).json()

    print(apiResponse)
    state = session["state"]
    set_state_findBus(state, payload)
    if(apiResponse['state']):
        session["state"]["tool_data"]["search_bus"] = {
        "results": apiResponse["buses"]
        }

    return apiResponse

@tool (description = SEARCH_BUS_DOCSTRING)
def search_bus(from_city: str, to_city: str, date: str | None, config: RunnableConfig):
    
    session = config["configurable"]["session"]

    payload = {
        "from": from_city,
        "to": to_city,
        "traveldate": date
    }

    return search_bus_api_call(payload , session)
