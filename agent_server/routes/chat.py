from flask import Blueprint, request, jsonify
from agent.agent import run_agent
from services.session import get_session

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/health")
def health():
    return {"status": "ok"}

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "default")
    message = data.get("message", "")

    session = get_session(user_id)
    result = run_agent(message, session)

    return jsonify(result)
