# ============================================================
# Auth routes — register (with OTP), login, password reset
# ============================================================
import re
import bcrypt
from flask import Blueprint, request, jsonify, g
from models import user as User, otp as Otp
from utils.jwt_utils import sign_token
from utils.mailer import send_mail, otp_email_template
from utils.decorators import require_auth

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = (data.get("email") or "").lower().strip()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"message": "Name, email and password are all required."}), 400
    if not EMAIL_RE.match(email):
        return jsonify({"message": "Please enter a valid email address."}), 400
    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters."}), 400

    existing = User.find_by_email(email)
    if existing and existing["is_verified"]:
        return jsonify({"message": "An account with this email already exists. Please log in."}), 409
    if existing and not existing["is_verified"]:
        User.delete_unverified(email)

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.create(name, email, password_hash)

    code = Otp.create(email, "register")
    try:
        send_mail(email, "Verify your InterviewIQ account", otp_email_template(name, code, "register"))
    except Exception as e:
        print(f"⚠️ Failed to send verification email: {e}")

    return jsonify({
        "message": "Account created. We've sent a 6-digit verification code to your email.",
        "email": email,
    }), 201


@auth_bp.post("/verify-otp")
def verify_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").lower().strip()
    code = data.get("code")

    if not email or not code:
        return jsonify({"message": "Email and code are required."}), 400

    ok, reason = Otp.verify(email, "register", code)
    if not ok:
        return jsonify({"message": reason}), 400

    User.mark_verified(email)
    user_row = User.find_by_email(email)

    token = sign_token({"id": user_row["id"], "email": user_row["email"]})
    return jsonify({
        "message": "Email verified! You're all set.",
        "token": token,
        "user": {"id": user_row["id"], "name": user_row["name"], "email": user_row["email"]},
    })


@auth_bp.post("/resend-otp")
def resend_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").lower().strip()
    if not email:
        return jsonify({"message": "Email is required."}), 400

    user_row = User.find_by_email(email)
    if not user_row:
        return jsonify({"message": "No pending registration found for this email."}), 404
    if user_row["is_verified"]:
        return jsonify({"message": "This account is already verified. Please log in."}), 400

    code = Otp.create(email, "register")
    try:
        send_mail(email, "Your new InterviewIQ verification code", otp_email_template(user_row["name"], code, "register"))
    except Exception as e:
        print(f"⚠️ Failed to send verification email: {e}")

    return jsonify({"message": "A new verification code has been sent to your email."})


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").lower().strip()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user_row = User.find_by_email(email)
    if not user_row:
        return jsonify({"message": "Invalid email or password."}), 401
    if not user_row["is_verified"]:
        return jsonify({
            "message": "Please verify your email before logging in.",
            "needsVerification": True,
            "email": user_row["email"],
        }), 403

    if not bcrypt.checkpw(password.encode(), user_row["password_hash"].encode()):
        return jsonify({"message": "Invalid email or password."}), 401

    token = sign_token({"id": user_row["id"], "email": user_row["email"]})
    return jsonify({
        "message": "Logged in successfully.",
        "token": token,
        "user": {"id": user_row["id"], "name": user_row["name"], "email": user_row["email"]},
    })


@auth_bp.post("/forgot-password")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").lower().strip()

    if not email or not EMAIL_RE.match(email):
        return jsonify({"message": "Please enter a valid email address."}), 400

    user_row = User.find_by_email(email)
    if user_row:
        code = Otp.create(email, "reset")
        try:
            send_mail(email, "Reset your InterviewIQ password", otp_email_template(user_row["name"], code, "reset"))
        except Exception as e:
            print(f"⚠️ Failed to send reset email: {e}")

    return jsonify({"message": "If an account exists for that email, a reset code has been sent."})


@auth_bp.post("/reset-password")
def reset_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").lower().strip()
    code = data.get("code")
    new_password = data.get("newPassword") or ""

    if not email or not code or not new_password:
        return jsonify({"message": "Email, code, and new password are all required."}), 400
    if len(new_password) < 8:
        return jsonify({"message": "Password must be at least 8 characters."}), 400

    ok, reason = Otp.verify(email, "reset", code)
    if not ok:
        return jsonify({"message": reason}), 400

    password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    User.update_password(email, password_hash)

    return jsonify({"message": "Password reset successfully. You can now log in."})


@auth_bp.get("/me")
@require_auth
def me():
    return jsonify({"user": g.user})
