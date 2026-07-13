# ============================================================
# Project routes — CRUD for the user's project list
# ============================================================
import os
import time
from flask import Blueprint, request, jsonify, g
from werkzeug.utils import secure_filename
from models import project as Project
from utils.decorators import require_auth
from config import Config

project_bp = Blueprint("project", __name__, url_prefix="/api/projects")

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp"}


@project_bp.get("/")
@require_auth
def list_projects():
    rows = Project.list_by_user(g.user["id"])
    return jsonify({"projects": rows})


@project_bp.post("/")
@require_auth
def create_project():
    data = request.get_json(silent=True) or {}
    new_id = Project.create(g.user["id"], data)
    return jsonify({"message": "Project added.", "id": new_id}), 201


@project_bp.put("/<int:project_id>")
@require_auth
def update_project(project_id):
    data = request.get_json(silent=True) or {}
    Project.update(g.user["id"], project_id, data)
    return jsonify({"message": "Project updated."})


@project_bp.post("/<int:project_id>/photo")
@require_auth
def upload_project_photo(project_id):
    if "photo" not in request.files:
        return jsonify({"message": "No photo file received."}), 400
    file = request.files["photo"]
    if file.filename == "" or "." not in file.filename or \
            file.filename.rsplit(".", 1)[1].lower() not in ALLOWED_IMAGE_EXT:
        return jsonify({"message": "Please upload a valid image file."}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{g.user['id']}_{int(time.time() * 1000)}.{ext}")
    dest_dir = os.path.join(Config.UPLOAD_DIR, "projects")
    os.makedirs(dest_dir, exist_ok=True)
    file.save(os.path.join(dest_dir, filename))

    relative_path = f"/uploads/projects/{filename}"
    Project.update_photo(g.user["id"], project_id, relative_path)
    return jsonify({"message": "Project photo updated!", "photo_path": relative_path})


@project_bp.delete("/<int:project_id>")
@require_auth
def delete_project(project_id):
    Project.remove(g.user["id"], project_id)
    return jsonify({"message": "Project removed."})
