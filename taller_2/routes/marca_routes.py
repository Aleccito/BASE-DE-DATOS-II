from flask import Blueprint

from controllers import marca_controller as controller

marca_bp = Blueprint("marca_bp", __name__, url_prefix="/api/marcas")

marca_bp.get("")(controller.list_marcas)
marca_bp.get("/<int:id_marca>")(controller.get_marca)
marca_bp.post("")(controller.create_marca)
marca_bp.put("/<int:id_marca>")(controller.update_marca)
marca_bp.delete("/<int:id_marca>")(controller.delete_marca)
