from services.session import add_to_history, print_history, update_state_from_llm
from agent.agent import create_search_agent
from utils.print import debug_print_messages
from services.llm import get_llm_summary
from services.key_manager import key_manager
import json 
from groq import BadRequestError
from langchain_core.messages import AIMessage
import time

# Remove global agent instantiation to ensure fresh LLM per request or retry
# agent = create_search_agent()


def handle_message(user_msg: str, session) -> str:
    history = session.get("history", [])
    state = session.get("state", {})

    state_context = f"""
    Current session state (source of truth):
    {json.dumps(state, indent=2)}

    Use this state to decide what tool to call or what to ask next.
    Do NOT invent values.
    """
    messages = [
        {"role": "system", "content": state_context},
        *history,
        {"role": "user", "content": user_msg},
    ]

    max_retries = len(key_manager.keys)
    attempts = 0
    result = None

    while attempts < max_retries:
        try:
            # Create a fresh agent which will use the current key from key_manager
            agent = create_search_agent()
            result = agent.invoke(
                {"messages": messages},
                config={"configurable": {"session": session}}
            )
            break # Success!
        except Exception as e:
            # Catch ResourceExhausted (rate limit) or PermissionDenied (bad key) by name
            error_type = type(e).__name__
            error_msg = str(e)
            
            if error_type in ["ResourceExhausted", "PermissionDenied"] or "429" in error_msg:
                attempts += 1
                if attempts >= max_retries:
                    return "I'm sorry, but I've reached my usage limit for now. Please try again later."
                
                print(f"Key {key_manager.get_key()[-5:]} exhausted or invalid ({error_type}). Switching... (Attempt {attempts})")
                key_manager.switch_key()
                continue # Retry the loop with the next key
            else:
                # If it's some other error, don't retry as it's likely a code or logic issue
                print(f"An unexpected error occurred: {error_type} - {error_msg}")
                return "I encountered an error while processing your request. Please try again."

    if not result:
        return "I'm having trouble connecting right now. Please try again in a moment."

    reply = ""
    last_message = result["messages"][-1]

    if isinstance(last_message, AIMessage):
        content = last_message.content

        # Gemini returns list of parts
        if isinstance(content, list):
            reply = "".join(
                part.get("text", "")
                for part in content
                if part.get("type") == "text"
            )
        else:
            reply = content or ""
    
    add_to_history(session, "user", user_msg)
    add_to_history(session, "assistant", reply)


    update_state_from_llm(session, get_llm_summary())


    return reply

