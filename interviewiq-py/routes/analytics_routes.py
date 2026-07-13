# ============================================================
# Analytics routes — interview session history
# ============================================================
from flask import Blueprint, request, jsonify, g
from models import session as Session
from utils.decorators import require_auth

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics_bp.get("/")
@require_auth
def list_sessions():
    rows = Session.list_by_user(g.user["id"])
    return jsonify({"sessions": rows})


@analytics_bp.post("/")
@require_auth
def create_session():
    data = request.get_json(silent=True) or {}
    avg_score = data.get("avgScore")
    total_qs = data.get("totalQs")
    categories = data.get("categories")

    if avg_score is None or total_qs is None:
        return jsonify({"message": "avgScore and totalQs are required."}), 400

    new_id = Session.create(g.user["id"], avg_score, total_qs, categories)
    return jsonify({"message": "Session saved!", "id": new_id}), 201
