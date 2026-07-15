"""
Helpers para estandarizar las respuestas JSON de la API.
"""
from flask import jsonify


def success_response(data=None, message="OK", status_code=200, meta=None):
    body = {"success": True, "message": message, "data": data}
    if meta is not None:
        body["meta"] = meta
    return jsonify(body), status_code


def error_response(message="Error", status_code=400, errors=None):
    body = {"success": False, "message": message}
    if errors is not None:
        body["errors"] = errors
    return jsonify(body), status_code
