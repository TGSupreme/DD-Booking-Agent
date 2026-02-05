from flask import Blueprint, request, jsonify
from agent.agent import run_agent
from services.session import get_session
from agent.executor import handle_message

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/health")
def health():
    return {"status": "ok"}

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    session = get_session(session_id)
    
    user_msg = data.get("message", "")

    reply = handle_message(user_msg, session)

    return jsonify({"reply": reply})
