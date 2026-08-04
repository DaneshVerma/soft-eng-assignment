from flask import Flask, Response
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.utils.responses import error_response

class APIError(Exception):
    """Base class for all API-related exceptions."""
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__()
        self.message = message
        self.status_code = status_code

class ValidationError(APIError):
    """Exception raised when input validation fails."""
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)

class NotFoundError(APIError):
    """Exception raised when a requested resource is not found."""
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)

def register_error_handlers(app: Flask) -> None:
    """
    Register all centralized error handlers for the Flask application.

    Args:
        app: The Flask application instance.
    """
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError) -> tuple[Response, int]:
        return error_response(error.message, error.status_code)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error: IntegrityError) -> tuple[Response, int]:
        # We try to handle duplicate data before getting here, but this is a safety net
        return error_response("Database integrity error, possibly duplicate data", 400)

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error: SQLAlchemyError) -> tuple[Response, int]:
        return error_response("A database error occurred", 500)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> tuple[Response, int]:
        # This catches 400 Bad Request (e.g. malformed JSON when using request.get_json())
        return error_response(str(error.description), error.code or 500)

    @app.errorhandler(Exception)
    def handle_generic_exception(error: Exception) -> tuple[Response, int]:
        return error_response("An unexpected error occurred", 500)
