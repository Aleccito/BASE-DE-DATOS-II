from flask import Blueprint

from controllers import aseguradora_controller as controller

aseguradora_bp = Blueprint("aseguradora_bp", __name__, url_prefix="/api/aseguradoras")

aseguradora_bp.get("")(controller.list_aseguradoras)
aseguradora_bp.get("/<int:id_aseguradora>")(controller.get_aseguradora)
aseguradora_bp.post("")(controller.create_aseguradora)
aseguradora_bp.put("/<int:id_aseguradora>")(controller.update_aseguradora)
aseguradora_bp.delete("/<int:id_aseguradora>")(controller.delete_aseguradora)
