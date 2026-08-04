from typing import Any
from flask import jsonify, Response

def success_response(data: Any = None, status_code: int = 200, **kwargs: Any) -> tuple[Response, int]:
    """
    Build a standardized success JSON response.

    Args:
        data: The payload to include in the 'data' field. Defaults to None.
        status_code: The HTTP status code to return. Defaults to 200.
        **kwargs: Additional fields to include at the root of the JSON response (e.g., pagination info).

    Returns:
        A tuple containing the Flask Response object and the HTTP status code.
    """
    payload: dict[str, Any] = {"success": True}
    
    if data is not None:
        payload["data"] = data
        
    if kwargs:
        payload.update(kwargs)
        
    return jsonify(payload), status_code

def error_response(message: str, status_code: int = 400) -> tuple[Response, int]:
    """
    Build a standardized error JSON response.

    Args:
        message: The error message to return.
        status_code: The HTTP status code to return. Defaults to 400.

    Returns:
        A tuple containing the Flask Response object and the HTTP status code.
    """
    return jsonify({
        "success": False,
        "error": message
    }), status_code
