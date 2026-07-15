from flask import Blueprint

from controllers import expediente_controller as controller

expediente_bp = Blueprint("expediente_bp", __name__, url_prefix="/api/expedientes")

expediente_bp.get("")(controller.list_expedientes)
expediente_bp.get("/<int:id_expediente>")(controller.get_expediente)
expediente_bp.post("")(controller.create_expediente)
expediente_bp.put("/<int:id_expediente>")(controller.update_expediente)
expediente_bp.delete("/<int:id_expediente>")(controller.delete_expediente)
