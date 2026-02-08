from flask import Blueprint, request, jsonify
from services.session import get_session, sessions, add_to_history
from agent.executor import handle_message
import uuid
from agent.agent import create_search_agent
from utils.print import debug_print_messages

agent = create_search_agent()
chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/health")
def health():
    return {"status": "ok"}

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = str(uuid.uuid4())
    session = get_session(session_id)
    # print(sessions)
    
    user_msg = data.get("message", "")

    # reply = handle_message(user_msg, session)
    result = agent.invoke({"messages": [{"role": "user", "content": user_msg}]})

    debug_print_messages(result["messages"])
    reply = result["messages"][-1].content

    add_to_history(session, "user", user_msg)
    add_to_history(session, "assistant", reply)
    
    return jsonify({"reply": reply})
