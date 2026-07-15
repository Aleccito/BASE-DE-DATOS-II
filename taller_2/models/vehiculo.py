from datetime import datetime

from extensions import db


class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id_vehiculo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario", ondelete="RESTRICT"), nullable=False)
    id_modelo = db.Column(db.Integer, db.ForeignKey("modelos.id_modelo", ondelete="RESTRICT"), nullable=False)
    id_marca = db.Column(db.Integer, db.ForeignKey("marcas.id_marca", ondelete="RESTRICT"), nullable=False)
    matricula = db.Column(db.String(20), nullable=False, unique=True)
    chasis = db.Column(db.String(50), nullable=False, unique=True)
    anio = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("anio BETWEEN 1900 AND 2100", name="chk_vehiculos_anio"),
    )

    usuario = db.relationship("Usuario", back_populates="vehiculos")
    modelo = db.relationship("Modelo", back_populates="vehiculos")
    marca = db.relationship("Marca", back_populates="vehiculos")
    expedientes = db.relationship("Expediente", back_populates="vehiculo")

    def to_dict(self):
        return {
            "id_vehiculo": self.id_vehiculo,
            "id_usuario": self.id_usuario,
            "id_modelo": self.id_modelo,
            "id_marca": self.id_marca,
            "matricula": self.matricula,
            "chasis": self.chasis,
            "anio": self.anio,
            "tipo": self.tipo,
            "color": self.color,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
