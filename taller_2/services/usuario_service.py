from extensions import db
from models.aseguradora import Aseguradora
from models.usuario import ROLES_VALIDOS, Usuario
from utils.validators import (
    ValidationError,
    validate_choice,
    validate_email,
    validate_int,
    validate_string,
)


def list_usuarios():
    return Usuario.query.order_by(Usuario.id_usuario).all()


def get_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        raise ValidationError(f"No existe un usuario con id {id_usuario}.")
    return usuario


def _validate_aseguradora(id_aseguradora):
    if id_aseguradora is None:
        return None
    if not Aseguradora.query.get(id_aseguradora):
        raise ValidationError(f"No existe una aseguradora con id {id_aseguradora}.")
    return id_aseguradora


def create_usuario(payload):
    nombre = validate_string(payload, "nombre", max_len=100)
    apellido = validate_string(payload, "apellido", max_len=100)
    identificacion = validate_string(payload, "identificacion", max_len=50)
    correo = validate_email(payload, "correo")
    password = payload.get("password")
    if not password or len(password) < 8:
        raise ValidationError("El campo 'password' es obligatorio y debe tener al menos 8 caracteres.")
    rol = validate_choice(payload, "rol", list(ROLES_VALIDOS), required=False, default="usuario")
    id_aseguradora = validate_int(payload, "id_aseguradora", required=False)
    id_aseguradora = _validate_aseguradora(id_aseguradora)

    if Usuario.query.filter_by(identificacion=identificacion).first():
        raise ValidationError("Ya existe un usuario con esa identificacion.")
    if Usuario.query.filter_by(correo=correo).first():
        raise ValidationError("Ya existe un usuario con ese correo.")

    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        identificacion=identificacion,
        correo=correo,
        rol=rol,
        id_aseguradora=id_aseguradora,
    )
    usuario.set_password(password)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def update_usuario(id_usuario, payload):
    usuario = get_usuario(id_usuario)

    if "nombre" in payload:
        usuario.nombre = validate_string(payload, "nombre", max_len=100)
    if "apellido" in payload:
        usuario.apellido = validate_string(payload, "apellido", max_len=100)
    if "identificacion" in payload:
        identificacion = validate_string(payload, "identificacion", max_len=50)
        duplicate = Usuario.query.filter(
            Usuario.identificacion == identificacion, Usuario.id_usuario != id_usuario
        ).first()
        if duplicate:
            raise ValidationError("Ya existe un usuario con esa identificacion.")
        usuario.identificacion = identificacion
    if "correo" in payload:
        correo = validate_email(payload, "correo")
        duplicate = Usuario.query.filter(
            Usuario.correo == correo, Usuario.id_usuario != id_usuario
        ).first()
        if duplicate:
            raise ValidationError("Ya existe un usuario con ese correo.")
        usuario.correo = correo
    if "rol" in payload:
        usuario.rol = validate_choice(payload, "rol", list(ROLES_VALIDOS))
    if "id_aseguradora" in payload:
        id_aseguradora = validate_int(payload, "id_aseguradora", required=False)
        usuario.id_aseguradora = _validate_aseguradora(id_aseguradora)
    if "password" in payload:
        password = payload.get("password")
        if not password or len(password) < 8:
            raise ValidationError("El campo 'password' debe tener al menos 8 caracteres.")
        usuario.set_password(password)

    db.session.commit()
    return usuario


def delete_usuario(id_usuario):
    usuario = get_usuario(id_usuario)
    if usuario.vehiculos or usuario.expedientes:
        raise ValidationError(
            "No se puede eliminar el usuario porque tiene vehiculos o expedientes asociados."
        )
    db.session.delete(usuario)
    db.session.commit()


def authenticate(correo, password):
    if not correo or not password:
        raise ValidationError("Correo y password son obligatorios.")
    usuario = Usuario.query.filter_by(correo=correo.strip().lower()).first()
    if not usuario or not usuario.check_password(password):
        raise ValidationError("Credenciales invalidas.")
    return usuario
