from extensions import db
from models.modelo import Modelo
from utils.validators import ValidationError, validate_string


def list_modelos():
    return Modelo.query.order_by(Modelo.id_modelo).all()


def get_modelo(id_modelo):
    modelo = Modelo.query.get(id_modelo)
    if not modelo:
        raise ValidationError(f"No existe un modelo con id {id_modelo}.")
    return modelo


def create_modelo(payload):
    nombre = validate_string(payload, "nombre", max_len=100)
    if Modelo.query.filter_by(nombre=nombre).first():
        raise ValidationError("Ya existe un modelo con ese nombre.")
    modelo = Modelo(nombre=nombre)
    db.session.add(modelo)
    db.session.commit()
    return modelo


def update_modelo(id_modelo, payload):
    modelo = get_modelo(id_modelo)
    if "nombre" in payload:
        nombre = validate_string(payload, "nombre", max_len=100)
        duplicate = Modelo.query.filter(Modelo.nombre == nombre, Modelo.id_modelo != id_modelo).first()
        if duplicate:
            raise ValidationError("Ya existe un modelo con ese nombre.")
        modelo.nombre = nombre
    db.session.commit()
    return modelo


def delete_modelo(id_modelo):
    modelo = get_modelo(id_modelo)
    if modelo.vehiculos:
        raise ValidationError("No se puede eliminar el modelo porque tiene vehiculos asociados.")
    db.session.delete(modelo)
    db.session.commit()
