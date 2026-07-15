"""
Decoradores reutilizables para las rutas de la API.
"""
from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from utils.responses import error_response


def roles_required(*roles):
    """Restringe el acceso a un endpoint a usuarios con alguno de los roles dados.

    Debe usarse junto con @jwt_required() (o despues de el) en la ruta.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return error_response("No tiene permisos para acceder a este recurso.", 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
