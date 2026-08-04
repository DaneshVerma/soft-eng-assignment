from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

class ValidationError(APIError):
    def __init__(self, message):
        super().__init__(message, status_code=400)

class NotFoundError(APIError):
    def __init__(self, message):
        super().__init__(message, status_code=404)

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify({"success": False, "error": error.message}), error.status_code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        # We try to handle duplicate data before getting here, but this is a safety net
        return jsonify({"success": False, "error": "Database integrity error, possibly duplicate data"}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        return jsonify({"success": False, "error": "A database error occurred"}), 500

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        # This catches 400 Bad Request (e.g. malformed JSON when using request.get_json())
        return jsonify({"success": False, "error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({"success": False, "error": "An unexpected error occurred"}), 500
