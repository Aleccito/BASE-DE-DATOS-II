from flask import request

from services import modelo_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


def list_modelos():
    items = service.list_modelos()
    return success_response([i.to_dict() for i in items])


def get_modelo(id_modelo):
    try:
        item = service.get_modelo(id_modelo)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


def create_modelo():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_modelo(payload)
        return success_response(item.to_dict(), "Modelo creado correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


def update_modelo(id_modelo):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_modelo(id_modelo, payload)
        return success_response(item.to_dict(), "Modelo actualizado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


def delete_modelo(id_modelo):
    try:
        service.delete_modelo(id_modelo)
        return success_response(None, "Modelo eliminado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)
