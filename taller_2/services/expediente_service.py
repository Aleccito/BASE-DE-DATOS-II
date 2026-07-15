from extensions import db
from models.aseguradora import Aseguradora
from models.expediente import ESTADOS_VALIDOS, Expediente
from models.juzgado import Juzgado
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from utils.validators import ValidationError, validate_choice, validate_int, validate_string


def list_expedientes():
    return Expediente.query.order_by(Expediente.id_expediente).all()


def get_expediente(id_expediente):
    expediente = Expediente.query.get(id_expediente)
    if not expediente:
        raise ValidationError(f"No existe un expediente con id {id_expediente}.")
    return expediente


def _validate_foreign_keys(id_aseguradora, id_juzgado, id_usuario, id_vehiculo):
    if not Aseguradora.query.get(id_aseguradora):
        raise ValidationError(f"No existe una aseguradora con id {id_aseguradora}.")
    if not Juzgado.query.get(id_juzgado):
        raise ValidationError(f"No existe un juzgado con id {id_juzgado}.")
    if not Usuario.query.get(id_usuario):
        raise ValidationError(f"No existe un usuario con id {id_usuario}.")
    if not Vehiculo.query.get(id_vehiculo):
        raise ValidationError(f"No existe un vehiculo con id {id_vehiculo}.")


def _parse_fecha(payload, required=True):
    from datetime import date

    value = payload.get("fecha")
    if value is None:
        if required:
            raise ValidationError("El campo 'fecha' es obligatorio (formato YYYY-MM-DD).")
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError("El campo 'fecha' debe tener el formato YYYY-MM-DD.")


def create_expediente(payload):
    id_aseguradora = validate_int(payload, "id_aseguradora")
    id_juzgado = validate_int(payload, "id_juzgado")
    id_usuario = validate_int(payload, "id_usuario")
    id_vehiculo = validate_int(payload, "id_vehiculo")
    estado = validate_choice(
        payload, "estado", list(ESTADOS_VALIDOS), required=False, default="abierto"
    )
    fecha = _parse_fecha(payload)

    _validate_foreign_keys(id_aseguradora, id_juzgado, id_usuario, id_vehiculo)

    expediente = Expediente(
        id_aseguradora=id_aseguradora,
        id_juzgado=id_juzgado,
        id_usuario=id_usuario,
        id_vehiculo=id_vehiculo,
        estado=estado,
        fecha=fecha,
    )
    db.session.add(expediente)
    db.session.commit()
    return expediente


def update_expediente(id_expediente, payload):
    expediente = get_expediente(id_expediente)

    id_aseguradora = validate_int(payload, "id_aseguradora", required=False) or expediente.id_aseguradora
    id_juzgado = validate_int(payload, "id_juzgado", required=False) or expediente.id_juzgado
    id_usuario = validate_int(payload, "id_usuario", required=False) or expediente.id_usuario
    id_vehiculo = validate_int(payload, "id_vehiculo", required=False) or expediente.id_vehiculo
    if any(k in payload for k in ("id_aseguradora", "id_juzgado", "id_usuario", "id_vehiculo")):
        _validate_foreign_keys(id_aseguradora, id_juzgado, id_usuario, id_vehiculo)

    if "estado" in payload:
        expediente.estado = validate_choice(payload, "estado", list(ESTADOS_VALIDOS))
    if "fecha" in payload:
        expediente.fecha = _parse_fecha(payload)

    expediente.id_aseguradora = id_aseguradora
    expediente.id_juzgado = id_juzgado
    expediente.id_usuario = id_usuario
    expediente.id_vehiculo = id_vehiculo

    db.session.commit()
    return expediente


def delete_expediente(id_expediente):
    expediente = get_expediente(id_expediente)
    db.session.delete(expediente)
    db.session.commit()
