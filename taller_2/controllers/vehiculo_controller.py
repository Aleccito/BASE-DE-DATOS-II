from flask import request
from flask_jwt_extended import jwt_required

from services import vehiculo_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


@jwt_required()
def list_vehiculos():
    items = service.list_vehiculos()
    return success_response([i.to_dict() for i in items])


@jwt_required()
def get_vehiculo(id_vehiculo):
    try:
        item = service.get_vehiculo(id_vehiculo)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


@jwt_required()
def create_vehiculo():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_vehiculo(payload)
        return success_response(item.to_dict(), "Vehiculo creado correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


@jwt_required()
def update_vehiculo(id_vehiculo):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_vehiculo(id_vehiculo, payload)
        return success_response(item.to_dict(), "Vehiculo actualizado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


@jwt_required()
def delete_vehiculo(id_vehiculo):
    try:
        service.delete_vehiculo(id_vehiculo)
        return success_response(None, "Vehiculo eliminado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)
