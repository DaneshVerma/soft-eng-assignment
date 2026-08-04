from flask import Flask, jsonify
from app.config import Config
from app.extensions import init_extensions
from app.errors import register_error_handlers

def create_app(config_class=Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)
    register_error_handlers(app)

    # Register models
    from app import models

    # Register blueprints
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "success": True,
            "message": "API running"
        })

    return app
