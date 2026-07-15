from flask import Blueprint

from controllers import vehiculo_controller as controller

vehiculo_bp = Blueprint("vehiculo_bp", __name__, url_prefix="/api/vehiculos")

vehiculo_bp.get("")(controller.list_vehiculos)
vehiculo_bp.get("/<int:id_vehiculo>")(controller.get_vehiculo)
vehiculo_bp.post("")(controller.create_vehiculo)
vehiculo_bp.put("/<int:id_vehiculo>")(controller.update_vehiculo)
vehiculo_bp.delete("/<int:id_vehiculo>")(controller.delete_vehiculo)
