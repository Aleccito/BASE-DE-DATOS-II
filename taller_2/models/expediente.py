from datetime import datetime

from extensions import db

ESTADOS_VALIDOS = ("abierto", "en_proceso", "cerrado", "archivado")


class Expediente(db.Model):
    __tablename__ = "expedientes"

    id_expediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aseguradora = db.Column(
        db.Integer, db.ForeignKey("aseguradoras.id_aseguradora", ondelete="RESTRICT"), nullable=False
    )
    id_juzgado = db.Column(db.Integer, db.ForeignKey("juzgados.id_juzgado", ondelete="RESTRICT"), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario", ondelete="RESTRICT"), nullable=False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey("vehiculos.id_vehiculo", ondelete="RESTRICT"), nullable=False)
    estado = db.Column(db.String(30), nullable=False, default="abierto")
    fecha = db.Column(db.Date, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint(
            "estado IN ('abierto','en_proceso','cerrado','archivado')",
            name="chk_expedientes_estado",
        ),
    )

    aseguradora = db.relationship("Aseguradora", back_populates="expedientes")
    juzgado = db.relationship("Juzgado", back_populates="expedientes")
    usuario = db.relationship("Usuario", back_populates="expedientes")
    vehiculo = db.relationship("Vehiculo", back_populates="expedientes")

    def to_dict(self):
        return {
            "id_expediente": self.id_expediente,
            "id_aseguradora": self.id_aseguradora,
            "id_juzgado": self.id_juzgado,
            "id_usuario": self.id_usuario,
            "id_vehiculo": self.id_vehiculo,
            "estado": self.estado,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
