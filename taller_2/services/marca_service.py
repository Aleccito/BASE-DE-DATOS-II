from extensions import db
from models.marca import Marca
from utils.validators import ValidationError, validate_string


def list_marcas():
    return Marca.query.order_by(Marca.id_marca).all()


def get_marca(id_marca):
    marca = Marca.query.get(id_marca)
    if not marca:
        raise ValidationError(f"No existe una marca con id {id_marca}.")
    return marca


def create_marca(payload):
    nombre = validate_string(payload, "nombre", max_len=100)
    if Marca.query.filter_by(nombre=nombre).first():
        raise ValidationError("Ya existe una marca con ese nombre.")
    marca = Marca(nombre=nombre)
    db.session.add(marca)
    db.session.commit()
    return marca


def update_marca(id_marca, payload):
    marca = get_marca(id_marca)
    if "nombre" in payload:
        nombre = validate_string(payload, "nombre", max_len=100)
        duplicate = Marca.query.filter(Marca.nombre == nombre, Marca.id_marca != id_marca).first()
        if duplicate:
            raise ValidationError("Ya existe una marca con ese nombre.")
        marca.nombre = nombre
    db.session.commit()
    return marca


def delete_marca(id_marca):
    marca = get_marca(id_marca)
    if marca.vehiculos:
        raise ValidationError("No se puede eliminar la marca porque tiene vehiculos asociados.")
    db.session.delete(marca)
    db.session.commit()
