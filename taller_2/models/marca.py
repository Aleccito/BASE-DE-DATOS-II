from datetime import datetime

from extensions import db


class Marca(db.Model):
    __tablename__ = "marcas"

    id_marca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    vehiculos = db.relationship("Vehiculo", back_populates="marca")

    def to_dict(self):
        return {
            "id_marca": self.id_marca,
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
