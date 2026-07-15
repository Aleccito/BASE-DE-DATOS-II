from flask import Blueprint

from controllers import juzgado_controller as controller

juzgado_bp = Blueprint("juzgado_bp", __name__, url_prefix="/api/juzgados")

juzgado_bp.get("")(controller.list_juzgados)
juzgado_bp.get("/<int:id_juzgado>")(controller.get_juzgado)
juzgado_bp.post("")(controller.create_juzgado)
juzgado_bp.put("/<int:id_juzgado>")(controller.update_juzgado)
juzgado_bp.delete("/<int:id_juzgado>")(controller.delete_juzgado)
