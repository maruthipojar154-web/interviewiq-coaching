# ============================================================
# require_auth — decorator that verifies JWT and attaches user to flask.g
# ============================================================
from functools import wraps
from flask import request, jsonify, g
import jwt as pyjwt
from utils.jwt_utils import verify_token
from models import user as User


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header[7:] if auth_header.startswith("Bearer ") else None

        if not token:
            return jsonify({"message": "Not authenticated. Please log in."}), 401

        try:
            decoded = verify_token(token)
        except pyjwt.ExpiredSignatureError:
            return jsonify({"message": "Your session expired. Please log in again."}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"message": "Invalid or expired session. Please log in again."}), 401

        user_row = User.find_by_id(decoded["id"])
        if not user_row:
            return jsonify({"message": "User no longer exists."}), 401

        g.user = {"id": user_row["id"], "name": user_row["name"], "email": user_row["email"]}
        return f(*args, **kwargs)

    return wrapper
