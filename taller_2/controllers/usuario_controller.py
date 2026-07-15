from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from services import usuario_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


@jwt_required()
def list_usuarios():
    items = service.list_usuarios()
    return success_response([i.to_dict() for i in items])


@jwt_required()
def get_usuario(id_usuario):
    try:
        item = service.get_usuario(id_usuario)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


def create_usuario():
    """Registro publico de un nuevo usuario."""
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_usuario(payload)
        return success_response(item.to_dict(), "Usuario creado correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


@jwt_required()
def update_usuario(id_usuario):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_usuario(id_usuario, payload)
        return success_response(item.to_dict(), "Usuario actualizado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


@jwt_required()
def delete_usuario(id_usuario):
    try:
        service.delete_usuario(id_usuario)
        return success_response(None, "Usuario eliminado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


@jwt_required()
def me():
    id_usuario = int(get_jwt_identity())
    item = service.get_usuario(id_usuario)
    return success_response(item.to_dict())
