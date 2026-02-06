from flask import Blueprint, request, jsonify
from services.session import get_session, sessions
from agent.executor import handle_message
import uuid

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/health")
def health():
    return {"status": "ok"}

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = str(uuid.uuid4())
    session = get_session(session_id)
    print(sessions)
    
    user_msg = data.get("message", "")

    reply = handle_message(user_msg, session)

    return jsonify({"reply": reply})
