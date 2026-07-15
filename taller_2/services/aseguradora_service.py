from extensions import db
from models.aseguradora import Aseguradora
from utils.validators import ValidationError, validate_string


def list_aseguradoras():
    return Aseguradora.query.order_by(Aseguradora.id_aseguradora).all()


def get_aseguradora(id_aseguradora):
    aseguradora = Aseguradora.query.get(id_aseguradora)
    if not aseguradora:
        raise ValidationError(f"No existe una aseguradora con id {id_aseguradora}.")
    return aseguradora


def create_aseguradora(payload):
    nombre = validate_string(payload, "nombre", max_len=150)
    if Aseguradora.query.filter_by(nombre=nombre).first():
        raise ValidationError("Ya existe una aseguradora con ese nombre.")
    aseguradora = Aseguradora(nombre=nombre)
    db.session.add(aseguradora)
    db.session.commit()
    return aseguradora


def update_aseguradora(id_aseguradora, payload):
    aseguradora = get_aseguradora(id_aseguradora)
    if "nombre" in payload:
        nombre = validate_string(payload, "nombre", max_len=150)
        duplicate = Aseguradora.query.filter(
            Aseguradora.nombre == nombre, Aseguradora.id_aseguradora != id_aseguradora
        ).first()
        if duplicate:
            raise ValidationError("Ya existe una aseguradora con ese nombre.")
        aseguradora.nombre = nombre
    db.session.commit()
    return aseguradora


def delete_aseguradora(id_aseguradora):
    aseguradora = get_aseguradora(id_aseguradora)
    if aseguradora.usuarios or aseguradora.expedientes:
        raise ValidationError(
            "No se puede eliminar la aseguradora porque tiene usuarios o expedientes asociados."
        )
    db.session.delete(aseguradora)
    db.session.commit()
