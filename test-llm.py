from agent_server.services.llm import get_llm
from langchain_core.messages import HumanMessage

llm = get_llm()

response = llm.invoke([
    # HumanMessage(content="Explain what a bus booking system does in 2 lines.")
    HumanMessage(content="whats todays date??")
])

print(response.content)
