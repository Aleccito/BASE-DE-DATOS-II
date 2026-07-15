from flask import request

from services import aseguradora_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


def list_aseguradoras():
    items = service.list_aseguradoras()
    return success_response([i.to_dict() for i in items])


def get_aseguradora(id_aseguradora):
    try:
        item = service.get_aseguradora(id_aseguradora)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


def create_aseguradora():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_aseguradora(payload)
        return success_response(item.to_dict(), "Aseguradora creada correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


def update_aseguradora(id_aseguradora):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_aseguradora(id_aseguradora, payload)
        return success_response(item.to_dict(), "Aseguradora actualizada correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


def delete_aseguradora(id_aseguradora):
    try:
        service.delete_aseguradora(id_aseguradora)
        return success_response(None, "Aseguradora eliminada correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)
