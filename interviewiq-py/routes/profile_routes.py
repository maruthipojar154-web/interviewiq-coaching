# ============================================================
# Profile routes — profile info, photo, resume uploads
# ============================================================
import os
import time
from flask import Blueprint, request, jsonify, g
from werkzeug.utils import secure_filename
from models import profile as Profile
from utils.decorators import require_auth
from config import Config

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_RESUME_EXT = {"pdf", "doc", "docx", "txt"}


def _ext_ok(filename, allowed):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@profile_bp.get("/")
@require_auth
def get_profile():
    row = Profile.get_by_user_id(g.user["id"])
    if row:
        return jsonify({"profile": row})
    return jsonify({"profile": {
        "role": "", "phone": "", "location": "", "linkedin": "", "github": "",
        "summary": "", "skills": [], "photo_path": None, "resume_text": "", "resume_path": None,
    }})


@profile_bp.put("/")
@require_auth
def update_profile():
    data = request.get_json(silent=True) or {}
    row = Profile.upsert(g.user["id"], data)
    return jsonify({"message": "Profile saved!", "profile": row})


@profile_bp.post("/photo")
@require_auth
def upload_photo():
    if "photo" not in request.files:
        return jsonify({"message": "No photo file received."}), 400
    file = request.files["photo"]
    if file.filename == "" or not _ext_ok(file.filename, ALLOWED_IMAGE_EXT):
        return jsonify({"message": "Please upload a valid image file (jpg, png, gif, webp)."}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{g.user['id']}_{int(time.time() * 1000)}.{ext}")
    dest_dir = os.path.join(Config.UPLOAD_DIR, "photos")
    os.makedirs(dest_dir, exist_ok=True)
    file.save(os.path.join(dest_dir, filename))

    relative_path = f"/uploads/photos/{filename}"
    Profile.update_photo(g.user["id"], relative_path)
    return jsonify({"message": "Photo updated!", "photo_path": relative_path})


@profile_bp.post("/resume")
@require_auth
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"message": "No resume file received."}), 400
    file = request.files["resume"]
    if file.filename == "" or not _ext_ok(file.filename, ALLOWED_RESUME_EXT):
        return jsonify({"message": "Please upload a PDF, DOC, DOCX, or TXT file."}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{g.user['id']}_{int(time.time() * 1000)}.{ext}")
    dest_dir = os.path.join(Config.UPLOAD_DIR, "resumes")
    os.makedirs(dest_dir, exist_ok=True)
    full_path = os.path.join(dest_dir, filename)
    file.save(full_path)

    # For .txt files, read text directly so the AI can use it as context.
    resume_text = ""
    if ext == "txt":
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                resume_text = f.read()[:8000]
        except Exception:
            resume_text = ""

    relative_path = f"/uploads/resumes/{filename}"
    Profile.update_resume(g.user["id"], resume_text, relative_path)
    return jsonify({"message": "Resume uploaded!", "resume_path": relative_path, "resume_text": resume_text})
