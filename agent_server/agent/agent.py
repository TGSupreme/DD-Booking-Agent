from services.llm import get_llm
from langchain.agents import create_agent

from tools.search_bus import search_bus
from tools.seats import get_all_seats_tool
from tools.create_ticket import create_ticket_tool
from tools.payment import complete_ticket_payment_tool


def create_search_agent():

    llm = get_llm()

    tools = [
        search_bus,
        get_all_seats_tool,
        create_ticket_tool,
        complete_ticket_payment_tool,
    ]

    agent = create_agent(
        model=llm.bind_tools(
            tools,
            tool_choice="auto"
        ),
        tools=tools,

        system_prompt = """
You are QuickBus, an intelligent bus booking assistant.

You can chat naturally with users and help them with:
- searching buses
- checking seat availability
- booking tickets
- completing payments
- answering general questions

You have access to tools that perform real backend actions.

RULES:

• Use a tool ONLY when real data or backend action is required
• NEVER fabricate bookings, seats, ticket IDs, or payments
• NEVER invent tools
• Ask for missing information before calling a tool
• If a question can be answered directly, respond without tools
• Use tool outputs as the single source of truth

Call tools only when necessary. Otherwise reply normally.
"""
    )

    return agent
