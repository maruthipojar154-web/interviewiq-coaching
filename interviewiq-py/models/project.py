# ============================================================
# Project model — many rows per user
# ============================================================
from extensions import query


def list_by_user(user_id):
    return query(
        "SELECT * FROM projects WHERE user_id = %s ORDER BY sort_order ASC, id ASC",
        (user_id,),
        fetchall=True,
    )


def create(user_id, data):
    return query(
        """INSERT INTO projects (user_id, name, stack, description, highlights, sort_order)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            user_id, data.get("name", ""), data.get("stack", ""),
            data.get("description", ""), data.get("highlights", ""), data.get("sortOrder", 0),
        ),
        commit=True,
    )


def update(user_id, project_id, data):
    query(
        """UPDATE projects SET name = %s, stack = %s, description = %s, highlights = %s
           WHERE id = %s AND user_id = %s""",
        (
            data.get("name", ""), data.get("stack", ""), data.get("description", ""),
            data.get("highlights", ""), project_id, user_id,
        ),
        commit=True,
    )


def update_photo(user_id, project_id, photo_path):
    query(
        "UPDATE projects SET photo_path = %s WHERE id = %s AND user_id = %s",
        (photo_path, project_id, user_id),
        commit=True,
    )


def remove(user_id, project_id):
    query("DELETE FROM projects WHERE id = %s AND user_id = %s", (project_id, user_id), commit=True)
