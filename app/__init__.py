from flask import Flask, jsonify
from app.config import Config
from app.extensions import init_extensions

def create_app(config_class=Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "success": True,
            "message": "API running"
        })

    return app
