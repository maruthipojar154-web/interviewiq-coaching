# ============================================================
# Page routes — serves the HTML pages (Flask renders templates)
# ============================================================
from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def index():
    return render_template("login.html")


@pages_bp.get("/login")
def login_page():
    return render_template("login.html")


@pages_bp.get("/register")
def register_page():
    return render_template("register.html")


@pages_bp.get("/verify-otp")
def verify_otp_page():
    return render_template("verify_otp.html")


@pages_bp.get("/forgot-password")
def forgot_password_page():
    return render_template("forgot_password.html")


@pages_bp.get("/reset-password")
def reset_password_page():
    return render_template("reset_password.html")


@pages_bp.get("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@pages_bp.get("/profile")
def profile_page():
    return render_template("profile.html")


@pages_bp.get("/resume")
def resume_page():
    return render_template("resume.html")


@pages_bp.get("/projects")
def projects_page():
    return render_template("projects.html")


@pages_bp.get("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")


@pages_bp.get("/analytics")
def analytics_page():
    return render_template("analytics.html")


@pages_bp.get("/voice-bot")
def voice_bot_page():
    return render_template("voice_bot.html")


@pages_bp.get("/chat-history")
def chat_history_page():
    return render_template("chat_history.html")
