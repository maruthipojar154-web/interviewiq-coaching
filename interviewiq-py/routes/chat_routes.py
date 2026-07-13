# ============================================================
# Chat routes — Groq AI + saves to chat history
# ============================================================
import requests
from flask import Blueprint, request, jsonify, g
from models import profile as Profile, project as Project
from models import chat_history as ChatHistory
from utils.decorators import require_auth
from config import Config

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")


def build_system_prompt(name, profile, projects):
    n = name or "the candidate"
    role = (profile or {}).get("role") or "Full-Stack Developer (Fresher)"
    skills = ", ".join((profile or {}).get("skills") or [])
    project_lines = "\n".join(
        f"- {p.get('name','')} | Stack: {p.get('stack','')} | {p.get('description','')} | Key: {p.get('highlights','')}"
        for p in projects
    )
    resume_text = (profile or {}).get("resume_text") or ""
    resume_block = f"\nRESUME:\n{resume_text[:3000]}" if resume_text else ""

    return f"""You are InterviewBot, a friendly AI interview coach for {n}.

CANDIDATE: Name: {n} | Role: {role} | Summary: {(profile or {}).get('summary', '')}
SKILLS: {skills}
PROJECTS:
{project_lines}{resume_block}

VOICE MODE: Keep responses SHORT (2-4 sentences max) and conversational — they will be READ ALOUD.
Avoid bullet points, markdown, or long lists in voice responses.

INTERVIEW MODE (triggered by "start interview","ask me","interview me"):
- Ask ONE question at a time
- After answer: give Score X out of 10 then brief feedback
- Tag category: Technical, Project, Behavioral, or HR
- Reference their real projects by name

COACH MODE (default): Answer prep questions, give tips, model answers.
STYLE: Warm, encouraging, concise. Always reference their actual projects."""


@chat_bp.post("/")
@require_auth
def send_message():
    if not Config.GROQ_API_KEY:
        return jsonify({"message": "AI service not configured. Set GROQ_API_KEY in .env"}), 500

    data = request.get_json(silent=True) or {}
    messages = data.get("messages")
    session_id = data.get("session_id")
    is_voice = data.get("voice", False)

    if not isinstance(messages, list) or len(messages) == 0:
        return jsonify({"message": "messages array is required."}), 400

    try:
        profile = Profile.get_by_user_id(g.user["id"])
        projects = Project.list_by_user(g.user["id"])
    except Exception as e:
        print(f"❌ Error loading profile/projects: {e}")
        return jsonify({"message": "Couldn't load your profile. Please try again."}), 500

    system_prompt = build_system_prompt(g.user["name"], profile, projects)

    # Add voice instruction to system if voice mode
    if is_voice:
        system_prompt += "\n\nIMPORTANT: This is a VOICE conversation. Keep reply under 3 sentences. No markdown."

    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {Config.GROQ_API_KEY}",
            },
            json={
                "model": Config.GROQ_MODEL,
                "max_tokens": 400 if is_voice else 1000,
                "messages": [{"role": "system", "content": system_prompt}, *messages],
            },
            timeout=30,
        )
    except requests.exceptions.Timeout:
        return jsonify({"message": "The AI took too long to respond. Please try again."}), 502
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error calling Groq: {e}")
        return jsonify({"message": "Couldn't reach the AI service. Check your internet connection."}), 502

    if not resp.ok:
        print(f"❌ Groq API error: {resp.status_code} {resp.text[:300]}")
        if resp.status_code == 401:
            msg = "Invalid Groq API key. Get a new one at console.groq.com and update .env"
        elif resp.status_code == 429:
            msg = "AI rate limit reached. Please wait a moment and try again."
        else:
            msg = "AI service unavailable. Please try again."
        payload = {"message": msg}
        if Config.FLASK_ENV != "production":
            payload["detail"] = resp.text[:300]
        return jsonify(payload), 502

    raw = resp.text
    if not raw or not raw.strip():
        return jsonify({"message": "AI returned an empty response. Please try again."}), 502

    try:
        body = resp.json()
    except ValueError:
        return jsonify({"message": "AI returned an unexpected response. Please try again."}), 502

    choices = body.get("choices") or []
    reply = choices[0]["message"]["content"] if choices and "message" in choices[0] else None
    if not reply:
        return jsonify({"message": "AI didn't return a usable response. Please try again."}), 502

    # Save to chat history if session_id provided
    if session_id:
        try:
            last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), None)
            if last_user_msg:
                ChatHistory.save_message(g.user["id"], session_id, "user", last_user_msg)
                ChatHistory.save_message(g.user["id"], session_id, "assistant", reply)
                # Auto-title session from first message
                sessions = ChatHistory.list_sessions(g.user["id"], limit=1)
                session = ChatHistory.get_session(session_id, g.user["id"])
                if session and session.get("title") == "New Chat":
                    title = last_user_msg[:60]
                    ChatHistory.update_session_title(session_id, title)
        except Exception as e:
            print(f"⚠️ Failed to save chat history: {e}")

    return jsonify({"reply": reply})
