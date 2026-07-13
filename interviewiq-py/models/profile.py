# ============================================================
# Profile model — one row per user
# ============================================================
import json
from extensions import query


def _safe_parse_skills(raw_skills):
    """
    mysql-connector-python returns JSON columns as plain strings (unlike mysql2 in
    Node, which auto-parses them). But we still guard against already-list values
    or empty/invalid strings, so this never throws even if the column was set
    inconsistently in the past.
    """
    if raw_skills is None:
        return []
    if isinstance(raw_skills, list):
        return raw_skills
    if isinstance(raw_skills, str) and raw_skills.strip():
        try:
            parsed = json.loads(raw_skills)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []
    return []


def get_by_user_id(user_id):
    row = query("SELECT * FROM profiles WHERE user_id = %s LIMIT 1", (user_id,), fetchone=True)
    if not row:
        return None
    row["skills"] = _safe_parse_skills(row.get("skills"))
    return row


def upsert(user_id, data):
    existing = get_by_user_id(user_id)
    skills_json = json.dumps(data.get("skills") or [])

    if existing:
        query(
            """UPDATE profiles SET
                role = %s, phone = %s, location = %s, linkedin = %s, github = %s,
                summary = %s, skills = %s
               WHERE user_id = %s""",
            (
                data.get("role", ""), data.get("phone", ""), data.get("location", ""),
                data.get("linkedin", ""), data.get("github", ""), data.get("summary", ""),
                skills_json, user_id,
            ),
            commit=True,
        )
    else:
        query(
            """INSERT INTO profiles (user_id, role, phone, location, linkedin, github, summary, skills)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                user_id, data.get("role", ""), data.get("phone", ""), data.get("location", ""),
                data.get("linkedin", ""), data.get("github", ""), data.get("summary", ""), skills_json,
            ),
            commit=True,
        )
    return get_by_user_id(user_id)


def update_photo(user_id, photo_path):
    query(
        """INSERT INTO profiles (user_id, photo_path) VALUES (%s, %s)
           ON DUPLICATE KEY UPDATE photo_path = %s""",
        (user_id, photo_path, photo_path),
        commit=True,
    )


def update_resume(user_id, resume_text, resume_path):
    query(
        """INSERT INTO profiles (user_id, resume_text, resume_path) VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE resume_text = %s, resume_path = %s""",
        (user_id, resume_text, resume_path, resume_text, resume_path),
        commit=True,
    )
