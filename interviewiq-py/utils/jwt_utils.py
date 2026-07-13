# ============================================================
# JWT helpers
# ============================================================
import jwt
from datetime import datetime, timedelta, timezone
from config import Config


def sign_token(payload):
    data = {
        **payload,
        "exp": datetime.now(timezone.utc) + timedelta(days=Config.JWT_EXPIRES_IN_DAYS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(data, Config.JWT_SECRET, algorithm="HS256")


def verify_token(token):
    return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
