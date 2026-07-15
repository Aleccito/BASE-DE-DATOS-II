from extensions import db
from models.marca import Marca
from models.modelo import Modelo
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from utils.validators import ValidationError, validate_int, validate_string


def list_vehiculos():
    return Vehiculo.query.order_by(Vehiculo.id_vehiculo).all()


def get_vehiculo(id_vehiculo):
    vehiculo = Vehiculo.query.get(id_vehiculo)
    if not vehiculo:
        raise ValidationError(f"No existe un vehiculo con id {id_vehiculo}.")
    return vehiculo


def _validate_foreign_keys(id_usuario, id_modelo, id_marca):
    if not Usuario.query.get(id_usuario):
        raise ValidationError(f"No existe un usuario con id {id_usuario}.")
    if not Modelo.query.get(id_modelo):
        raise ValidationError(f"No existe un modelo con id {id_modelo}.")
    if not Marca.query.get(id_marca):
        raise ValidationError(f"No existe una marca con id {id_marca}.")


def create_vehiculo(payload):
    id_usuario = validate_int(payload, "id_usuario")
    id_modelo = validate_int(payload, "id_modelo")
    id_marca = validate_int(payload, "id_marca")
    matricula = validate_string(payload, "matricula", max_len=20)
    chasis = validate_string(payload, "chasis", max_len=50)
    anio = validate_int(payload, "anio", min_value=1900, max_value=2100)
    tipo = validate_string(payload, "tipo", max_len=50)
    color = validate_string(payload, "color", max_len=30)

    _validate_foreign_keys(id_usuario, id_modelo, id_marca)

    if Vehiculo.query.filter_by(matricula=matricula).first():
        raise ValidationError("Ya existe un vehiculo con esa matricula.")
    if Vehiculo.query.filter_by(chasis=chasis).first():
        raise ValidationError("Ya existe un vehiculo con ese chasis.")

    vehiculo = Vehiculo(
        id_usuario=id_usuario,
        id_modelo=id_modelo,
        id_marca=id_marca,
        matricula=matricula,
        chasis=chasis,
        anio=anio,
        tipo=tipo,
        color=color,
    )
    db.session.add(vehiculo)
    db.session.commit()
    return vehiculo


def update_vehiculo(id_vehiculo, payload):
    vehiculo = get_vehiculo(id_vehiculo)

    id_usuario = validate_int(payload, "id_usuario", required=False) or vehiculo.id_usuario
    id_modelo = validate_int(payload, "id_modelo", required=False) or vehiculo.id_modelo
    id_marca = validate_int(payload, "id_marca", required=False) or vehiculo.id_marca
    if any(k in payload for k in ("id_usuario", "id_modelo", "id_marca")):
        _validate_foreign_keys(id_usuario, id_modelo, id_marca)

    if "matricula" in payload:
        matricula = validate_string(payload, "matricula", max_len=20)
        duplicate = Vehiculo.query.filter(
            Vehiculo.matricula == matricula, Vehiculo.id_vehiculo != id_vehiculo
        ).first()
        if duplicate:
            raise ValidationError("Ya existe un vehiculo con esa matricula.")
        vehiculo.matricula = matricula
    if "chasis" in payload:
        chasis = validate_string(payload, "chasis", max_len=50)
        duplicate = Vehiculo.query.filter(
            Vehiculo.chasis == chasis, Vehiculo.id_vehiculo != id_vehiculo
        ).first()
        if duplicate:
            raise ValidationError("Ya existe un vehiculo con ese chasis.")
        vehiculo.chasis = chasis
    if "anio" in payload:
        vehiculo.anio = validate_int(payload, "anio", min_value=1900, max_value=2100)
    if "tipo" in payload:
        vehiculo.tipo = validate_string(payload, "tipo", max_len=50)
    if "color" in payload:
        vehiculo.color = validate_string(payload, "color", max_len=30)

    vehiculo.id_usuario = id_usuario
    vehiculo.id_modelo = id_modelo
    vehiculo.id_marca = id_marca

    db.session.commit()
    return vehiculo


def delete_vehiculo(id_vehiculo):
    vehiculo = get_vehiculo(id_vehiculo)
    if vehiculo.expedientes:
        raise ValidationError("No se puede eliminar el vehiculo porque tiene expedientes asociados.")
    db.session.delete(vehiculo)
    db.session.commit()
