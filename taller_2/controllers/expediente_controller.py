from flask import request
from flask_jwt_extended import jwt_required

from services import expediente_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


@jwt_required()
def list_expedientes():
    items = service.list_expedientes()
    return success_response([i.to_dict() for i in items])


@jwt_required()
def get_expediente(id_expediente):
    try:
        item = service.get_expediente(id_expediente)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


@jwt_required()
def create_expediente():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_expediente(payload)
        return success_response(item.to_dict(), "Expediente creado correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


@jwt_required()
def update_expediente(id_expediente):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_expediente(id_expediente, payload)
        return success_response(item.to_dict(), "Expediente actualizado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


@jwt_required()
def delete_expediente(id_expediente):
    try:
        service.delete_expediente(id_expediente)
        return success_response(None, "Expediente eliminado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)
