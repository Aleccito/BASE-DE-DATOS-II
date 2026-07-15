from flask import Blueprint

from controllers import modelo_controller as controller

modelo_bp = Blueprint("modelo_bp", __name__, url_prefix="/api/modelos")

modelo_bp.get("")(controller.list_modelos)
modelo_bp.get("/<int:id_modelo>")(controller.get_modelo)
modelo_bp.post("")(controller.create_modelo)
modelo_bp.put("/<int:id_modelo>")(controller.update_modelo)
modelo_bp.delete("/<int:id_modelo>")(controller.delete_modelo)
