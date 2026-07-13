# ============================================================
# Chat history model
# ============================================================
import uuid
import json
from extensions import query


def create_session(user_id, title="New Chat"):
    session_id = str(uuid.uuid4())
    query(
        "INSERT INTO chat_sessions (id, user_id, title) VALUES (%s, %s, %s)",
        (session_id, user_id, title),
        commit=True,
    )
    return session_id


def update_session_title(session_id, title):
    query(
        "UPDATE chat_sessions SET title = %s WHERE id = %s",
        (title[:80], session_id),
        commit=True,
    )


def list_sessions(user_id, limit=30):
    return query(
        """SELECT id, title, created_at, updated_at
           FROM chat_sessions WHERE user_id = %s
           ORDER BY updated_at DESC LIMIT %s""",
        (user_id, limit),
        fetchall=True,
    ) or []


def get_session(session_id, user_id):
    return query(
        "SELECT * FROM chat_sessions WHERE id = %s AND user_id = %s",
        (session_id, user_id),
        fetchone=True,
    )


def save_message(user_id, session_id, role, content):
    query(
        "INSERT INTO chat_messages (user_id, session_id, role, content) VALUES (%s, %s, %s, %s)",
        (user_id, session_id, role, content),
        commit=True,
    )
    # Update session timestamp
    query(
        "UPDATE chat_sessions SET updated_at = NOW() WHERE id = %s",
        (session_id,),
        commit=True,
    )


def get_messages(session_id, user_id):
    return query(
        """SELECT role, content, created_at FROM chat_messages
           WHERE session_id = %s AND user_id = %s
           ORDER BY id ASC""",
        (session_id, user_id),
        fetchall=True,
    ) or []


def delete_session(session_id, user_id):
    query(
        "DELETE FROM chat_messages WHERE session_id = %s AND user_id = %s",
        (session_id, user_id),
        commit=True,
    )
    query(
        "DELETE FROM chat_sessions WHERE id = %s AND user_id = %s",
        (session_id, user_id),
        commit=True,
    )
