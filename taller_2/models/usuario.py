from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db

ROLES_VALIDOS = ("usuario", "admin")


class Usuario(db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aseguradora = db.Column(
        db.Integer, db.ForeignKey("aseguradoras.id_aseguradora", ondelete="SET NULL"), nullable=True
    )
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    identificacion = db.Column(db.String(50), nullable=False, unique=True)
    correo = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="usuario")
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    aseguradora = db.relationship("Aseguradora", back_populates="usuarios")
    vehiculos = db.relationship("Vehiculo", back_populates="usuario")
    expedientes = db.relationship("Expediente", back_populates="usuario")

    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self, include_sensitive=False):
        data = {
            "id_usuario": self.id_usuario,
            "id_aseguradora": self.id_aseguradora,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "identificacion": self.identificacion,
            "correo": self.correo,
            "rol": self.rol,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }
        return data
