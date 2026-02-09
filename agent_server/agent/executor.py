from agent.action_router import route_action
from agent.intent_router import route_intent
from services.session import add_to_history, print_history
from agent.handler.handle_conversation import handle_conversation
from agent.agent import create_search_agent
from utils.print import debug_print_messages

agent = create_search_agent()



def handle_message(user_msg: str, session) -> str:
    reply = None

    result = agent.invoke({"messages": [{"role": "user", "content": user_msg}]},
                          config={"configurable": {"session": session}})

    debug_print_messages(result["messages"])
    reply = result["messages"][-1].content

    add_to_history(session, "user", user_msg)
    add_to_history(session, "assistant", reply)

    
    return reply
