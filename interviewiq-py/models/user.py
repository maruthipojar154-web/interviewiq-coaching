# ============================================================
# User model
# ============================================================
from extensions import query


def find_by_email(email):
    return query("SELECT * FROM users WHERE email = %s LIMIT 1", (email,), fetchone=True)


def find_by_id(user_id):
    return query("SELECT * FROM users WHERE id = %s LIMIT 1", (user_id,), fetchone=True)


def create(name, email, password_hash):
    return query(
        "INSERT INTO users (name, email, password_hash, is_verified) VALUES (%s, %s, %s, 0)",
        (name, email, password_hash),
        commit=True,
    )


def mark_verified(email):
    query("UPDATE users SET is_verified = 1 WHERE email = %s", (email,), commit=True)


def update_password(email, password_hash):
    query("UPDATE users SET password_hash = %s WHERE email = %s", (password_hash, email), commit=True)


def delete_unverified(email):
    query("DELETE FROM users WHERE email = %s AND is_verified = 0", (email,), commit=True)
