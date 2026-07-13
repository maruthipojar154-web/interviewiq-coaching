# ============================================================
# OTP model — email verification & password reset codes
# ============================================================
import random
import bcrypt
from datetime import datetime, timedelta
from extensions import query
from config import Config


def generate_code():
    return str(random.randint(100000, 999999))


def create(email, purpose):
    code = generate_code()
    code_hash = bcrypt.hashpw(code.encode(), bcrypt.gensalt()).decode()
    expires_at = datetime.now() + timedelta(minutes=Config.OTP_EXPIRY_MINUTES)

    # Invalidate previous unused OTPs for this email + purpose
    query(
        "UPDATE otp_codes SET used = 1 WHERE email = %s AND purpose = %s AND used = 0",
        (email, purpose),
        commit=True,
    )

    query(
        "INSERT INTO otp_codes (email, code_hash, purpose, expires_at) VALUES (%s, %s, %s, %s)",
        (email, code_hash, purpose, expires_at),
        commit=True,
    )
    return code  # plaintext, to be emailed


def verify(email, purpose, code):
    record = query(
        """SELECT * FROM otp_codes
           WHERE email = %s AND purpose = %s AND used = 0
           ORDER BY id DESC LIMIT 1""",
        (email, purpose),
        fetchone=True,
    )
    if not record:
        return False, "No OTP found. Please request a new code."

    if record["expires_at"] < datetime.now():
        return False, "This code has expired. Please request a new one."

    if not bcrypt.checkpw(code.encode(), record["code_hash"].encode()):
        return False, "Incorrect code. Please try again."

    query("UPDATE otp_codes SET used = 1 WHERE id = %s", (record["id"],), commit=True)
    return True, None
