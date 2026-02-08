from services.llm import get_llm
from langchain.agents import create_agent
from tools.search_bus import search_bus


def create_search_agent():

    llm = get_llm()

    tools = [search_bus]

    agent = create_agent(
        model=llm.bind_tools(
            tools,
            tool_choice="auto"   # or "required"
        ),   # bind tools to HF model
        tools=tools,
        system_prompt="""
        You are QuickBus assistant.

        CRITICAL RULES:
        - You have access to EXACTLY ONE tool: `search_bus`
        - NO other tools exist
        - You MUST NOT invent tools
        - You MUST NOT use web search
        - You MUST NOT use browsing tools
        - For any bus-related query, ONLY call `search_bus`
        - If required information is missing, ask the user instead of calling a tool

        """

    )

    return agent
