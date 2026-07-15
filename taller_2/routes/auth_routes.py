from flask import Blueprint

from controllers import auth_controller as controller

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

auth_bp.post("/register")(controller.register)
auth_bp.post("/login")(controller.login)
auth_bp.post("/refresh")(controller.refresh)
