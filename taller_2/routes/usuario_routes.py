from flask import Blueprint

from controllers import usuario_controller as controller

usuario_bp = Blueprint("usuario_bp", __name__, url_prefix="/api/usuarios")

usuario_bp.get("")(controller.list_usuarios)
usuario_bp.get("/me")(controller.me)
usuario_bp.get("/<int:id_usuario>")(controller.get_usuario)
usuario_bp.post("")(controller.create_usuario)
usuario_bp.put("/<int:id_usuario>")(controller.update_usuario)
usuario_bp.delete("/<int:id_usuario>")(controller.delete_usuario)
