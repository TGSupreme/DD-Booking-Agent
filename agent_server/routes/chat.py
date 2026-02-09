from flask import Blueprint, request, jsonify
from services.session import get_session, sessions, add_to_history
from agent.executor import handle_message
import uuid

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/health")
def health():
    return {"status": "ok"}

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    session = get_session(session_id)
    # print(sessions)
    
    user_msg = data.get("message", "")

    reply = handle_message(user_msg, session)
    
    
    return jsonify({"reply": reply})
