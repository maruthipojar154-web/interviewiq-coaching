# ============================================================
# Chat history routes
# ============================================================
from flask import Blueprint, request, jsonify, g
from models import chat_history as ChatHistory
from utils.decorators import require_auth

chat_history_bp = Blueprint("chat_history", __name__, url_prefix="/api/chat-history")


@chat_history_bp.get("/sessions")
@require_auth
def list_sessions():
    sessions = ChatHistory.list_sessions(g.user["id"])
    return jsonify({"sessions": sessions})


@chat_history_bp.post("/sessions")
@require_auth
def create_session():
    data = request.get_json(silent=True) or {}
    session_id = ChatHistory.create_session(g.user["id"], data.get("title", "New Chat"))
    return jsonify({"session_id": session_id}), 201


@chat_history_bp.get("/sessions/<session_id>")
@require_auth
def get_messages(session_id):
    session = ChatHistory.get_session(session_id, g.user["id"])
    if not session:
        return jsonify({"message": "Session not found."}), 404
    messages = ChatHistory.get_messages(session_id, g.user["id"])
    return jsonify({"session": session, "messages": messages})


@chat_history_bp.delete("/sessions/<session_id>")
@require_auth
def delete_session(session_id):
    ChatHistory.delete_session(session_id, g.user["id"])
    return jsonify({"message": "Conversation deleted."})
