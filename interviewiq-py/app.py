# ============================================================
# InterviewIQ — Flask application entry point
# ============================================================
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from config import Config
from extensions import init_pool

from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.project_routes import project_bp
from routes.chat_routes import chat_bp
from routes.analytics_routes import analytics_bp
from routes.page_routes import pages_bp
from routes.chat_history_routes import chat_history_bp


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

    CORS(app, supports_credentials=True, origins=["*"])
    init_pool()

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(chat_history_bp)

    @app.route("/uploads/<path:subpath>")
    def uploaded_file(subpath):
        return send_from_directory(Config.UPLOAD_DIR, subpath)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Route not found."}), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"❌ Unhandled error: {e}")
        return jsonify({"message": "Something went wrong on the server. Please try again."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    os.makedirs(os.path.join(Config.UPLOAD_DIR, "photos"), exist_ok=True)
    os.makedirs(os.path.join(Config.UPLOAD_DIR, "resumes"), exist_ok=True)
    os.makedirs(os.path.join(Config.UPLOAD_DIR, "projects"), exist_ok=True)
    port = int(os.environ.get("PORT", Config.PORT))
    print(f"🚀 InterviewIQ running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
