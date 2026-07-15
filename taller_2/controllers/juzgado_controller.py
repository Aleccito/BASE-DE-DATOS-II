from flask import request

from services import juzgado_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


def list_juzgados():
    items = service.list_juzgados()
    return success_response([i.to_dict() for i in items])


def get_juzgado(id_juzgado):
    try:
        item = service.get_juzgado(id_juzgado)
        return success_response(item.to_dict())
    except ValidationError as e:
        return error_response(str(e), 404, e.errors)


def create_juzgado():
    payload = request.get_json(silent=True) or {}
    try:
        item = service.create_juzgado(payload)
        return success_response(item.to_dict(), "Juzgado creado correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


def update_juzgado(id_juzgado):
    payload = request.get_json(silent=True) or {}
    try:
        item = service.update_juzgado(id_juzgado, payload)
        return success_response(item.to_dict(), "Juzgado actualizado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)


def delete_juzgado(id_juzgado):
    try:
        service.delete_juzgado(id_juzgado)
        return success_response(None, "Juzgado eliminado correctamente.")
    except ValidationError as e:
        status = 404 if "No existe" in str(e) else 400
        return error_response(str(e), status, e.errors)
