from datetime import datetime

from extensions import db


class Juzgado(db.Model):
    __tablename__ = "juzgados"

    id_juzgado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    region = db.Column(db.String(100), nullable=False)
    numero_de_juzgado = db.Column(db.String(50), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("region", "numero_de_juzgado", name="uq_juzgados_region_numero"),
    )

    expedientes = db.relationship("Expediente", back_populates="juzgado")

    def to_dict(self):
        return {
            "id_juzgado": self.id_juzgado,
            "region": self.region,
            "numero_de_juzgado": self.numero_de_juzgado,
            "ubicacion": self.ubicacion,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
