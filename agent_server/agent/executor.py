from services.session import add_to_history, print_history, update_state_from_llm
from agent.agent import create_search_agent
from utils.print import debug_print_messages
from services.llm import get_llm
import json 
from groq import BadRequestError

agent = create_search_agent()



def handle_message(user_msg: str, session) -> str:

    history = session.get("history", [])
    state = session.get("state", {})


    # convert state → readable text for LLM
    state_context = f"""
    Current session state (source of truth):
    {json.dumps(state, indent=2)}

    Use this state to decide what tool to call or what to ask next.
    Do NOT invent values.
    """
    messages = [
        {"role": "system", "content": state_context},
        *history,  # past messages
        {"role": "user", "content": user_msg},
    ]

    
    # try:
    #     result = agent.invoke(
    #         {"messages": messages},
    #         config={"configurable": {"session": session}})
    # except BadRequestError:
    #     print(f"ERROR----> : {BadRequestError}")
    #     print("(BadRequestError occured) Retrying...")
    result = agent.invoke(
        {"messages": messages},
        config={"configurable": {"session": session}})

    debug_print_messages(result["messages"])

    reply = result["messages"][-1].content
    add_to_history(session, "user", user_msg)
    add_to_history(session, "assistant", reply)

    #update states from conversation history
    update_state_from_llm(session, get_llm())
    # print_state(state)

    return reply

