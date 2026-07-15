from flask import request

from services import marca_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


def list_marcas():
    items = service.list_marcas()
    return success_response([i.to_dict() for i in items])


def get_marca(id_marca):
    try:
        item = service.get_marca(id_marca)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


def create_marca():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_marca(payload)
        return success_response(item.to_dict(), "Marca creada correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


def update_marca(id_marca):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_marca(id_marca, payload)
        return success_response(item.to_dict(), "Marca actualizada correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


def delete_marca(id_marca):
    try:
        service.delete_marca(id_marca)
        return success_response(None, "Marca eliminada correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)
