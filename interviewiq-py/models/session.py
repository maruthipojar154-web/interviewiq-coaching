# ============================================================
# Session model — interview session history, for analytics
# ============================================================
import json
from extensions import query


def _safe_parse_categories(raw):
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}
    return {}


def list_by_user(user_id, limit=30):
    rows = query(
        "SELECT * FROM sessions WHERE user_id = %s ORDER BY id DESC LIMIT %s",
        (user_id, limit),
        fetchall=True,
    )
    for r in rows:
        r["categories"] = _safe_parse_categories(r.get("categories"))
    return list(reversed(rows))


def create(user_id, avg_score, total_qs, categories):
    return query(
        "INSERT INTO sessions (user_id, avg_score, total_qs, categories) VALUES (%s, %s, %s, %s)",
        (user_id, avg_score, total_qs, json.dumps(categories or {})),
        commit=True,
    )
