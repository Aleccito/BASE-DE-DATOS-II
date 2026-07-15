from extensions import db
from models.juzgado import Juzgado
from utils.validators import ValidationError, validate_string


def list_juzgados():
    return Juzgado.query.order_by(Juzgado.id_juzgado).all()


def get_juzgado(id_juzgado):
    juzgado = Juzgado.query.get(id_juzgado)
    if not juzgado:
        raise ValidationError(f"No existe un juzgado con id {id_juzgado}.")
    return juzgado


def _check_duplicate(region, numero_de_juzgado, exclude_id=None):
    query = Juzgado.query.filter_by(region=region, numero_de_juzgado=numero_de_juzgado)
    if exclude_id is not None:
        query = query.filter(Juzgado.id_juzgado != exclude_id)
    if query.first():
        raise ValidationError("Ya existe un juzgado con esa region y numero de juzgado.")


def create_juzgado(payload):
    region = validate_string(payload, "region", max_len=100)
    numero_de_juzgado = validate_string(payload, "numero_de_juzgado", max_len=50)
    ubicacion = validate_string(payload, "ubicacion", max_len=200)
    _check_duplicate(region, numero_de_juzgado)

    juzgado = Juzgado(region=region, numero_de_juzgado=numero_de_juzgado, ubicacion=ubicacion)
    db.session.add(juzgado)
    db.session.commit()
    return juzgado


def update_juzgado(id_juzgado, payload):
    juzgado = get_juzgado(id_juzgado)
    region = validate_string(payload, "region", max_len=100, required=False) or juzgado.region
    numero_de_juzgado = (
        validate_string(payload, "numero_de_juzgado", max_len=50, required=False)
        or juzgado.numero_de_juzgado
    )
    if "region" in payload or "numero_de_juzgado" in payload:
        _check_duplicate(region, numero_de_juzgado, exclude_id=id_juzgado)
    if "ubicacion" in payload:
        juzgado.ubicacion = validate_string(payload, "ubicacion", max_len=200)
    juzgado.region = region
    juzgado.numero_de_juzgado = numero_de_juzgado
    db.session.commit()
    return juzgado


def delete_juzgado(id_juzgado):
    juzgado = get_juzgado(id_juzgado)
    if juzgado.expedientes:
        raise ValidationError("No se puede eliminar el juzgado porque tiene expedientes asociados.")
    db.session.delete(juzgado)
    db.session.commit()
