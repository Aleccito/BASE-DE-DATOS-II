"""
Paquete de modelos SQLAlchemy.

Se importan todos los modelos aqui para que Flask-Migrate/Alembic
los detecte correctamente al generar migraciones.
"""
from models.aseguradora import Aseguradora
from models.juzgado import Juzgado
from models.marca import Marca
from models.modelo import Modelo
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.expediente import Expediente

__all__ = [
    "Aseguradora",
    "Juzgado",
    "Marca",
    "Modelo",
    "Usuario",
    "Vehiculo",
    "Expediente",
]
