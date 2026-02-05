from services.llm import get_llm\


llm = get_llm()

def run_agent(message: str, session):
    """
    Placeholder only.
    Later:
    - call LLM
    - extract intent
    - choose tool
    """
    return {
        "reply": "Agent wiring ready. Logic not implemented yet."
    }
