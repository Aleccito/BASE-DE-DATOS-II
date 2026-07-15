from datetime import datetime

from extensions import db


class Aseguradora(db.Model):
    __tablename__ = "aseguradoras"

    id_aseguradora = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False, unique=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    usuarios = db.relationship("Usuario", back_populates="aseguradora")
    expedientes = db.relationship("Expediente", back_populates="aseguradora")

    def to_dict(self):
        return {
            "id_aseguradora": self.id_aseguradora,
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
