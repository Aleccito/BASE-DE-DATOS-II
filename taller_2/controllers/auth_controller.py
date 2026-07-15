from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from services import usuario_service as service
from utils.responses import error_response, success_response
from utils.validators import ValidationError


def register():
    """Alias de registro publico (equivalente a crear un usuario)."""
    payload = request.get_json(silent=True) or {}
    try:
        usuario = service.create_usuario(payload)
        return success_response(usuario.to_dict(), "Usuario registrado correctamente.", 201)
    except ValidationError as e:
        return error_response("Datos invalidos.", 400, e.errors)


def login():
    payload = request.get_json(silent=True) or {}
    try:
        usuario = service.authenticate(payload.get("correo"), payload.get("password"))
    except ValidationError as e:
        return error_response(str(e), 401, e.errors)

    extra_claims = {"rol": usuario.rol, "correo": usuario.correo}
    access_token = create_access_token(identity=str(usuario.id_usuario), additional_claims=extra_claims)
    refresh_token = create_refresh_token(identity=str(usuario.id_usuario), additional_claims=extra_claims)
    return success_response(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "usuario": usuario.to_dict(),
        },
        "Inicio de sesion exitoso.",
    )


@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    usuario = service.get_usuario(int(identity))
    extra_claims = {"rol": usuario.rol, "correo": usuario.correo}
    access_token = create_access_token(identity=identity, additional_claims=extra_claims)
    return success_response({"access_token": access_token}, "Token renovado correctamente.")
