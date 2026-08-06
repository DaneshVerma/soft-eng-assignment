from typing import Type
from flask import Flask, Response
from app.config import Config
from app.extensions import init_extensions
from app.errors import register_error_handlers
from app.utils.responses import success_response

def create_app(config_class: Type[Config] = Config) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_class: The configuration class to use. Defaults to Config.

    Returns:
        The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)
    register_error_handlers(app)

    # Register models (ensures they are known to SQLAlchemy before routes load)
    from app import models

    # Register blueprints
    from app.routes import user_bp, auth_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    @app.route("/", methods=["GET"])
    def health_check() -> tuple[Response, int]:
        """
        API health check endpoint.
        """
        return success_response(message="API running", status_code=200)

    return app
