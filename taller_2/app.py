"""
Punto de entrada de la aplicacion Flask.

Ejecutar con:
    python app.py
o bien:
    flask run
"""
import os

from flask import Flask

from config import config_by_name
from extensions import cors, db, jwt, migrate
from routes import register_routes
from utils.responses import error_response


def create_app(env_name=None):
    env_name = env_name or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(env_name, config_by_name["development"]))

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Modelos (necesarios para que Flask-Migrate los detecte)
    import models  # noqa: F401

    # Rutas
    register_routes(app)

    register_error_handlers(app)
    register_health_check(app)

    return app


def register_health_check(app):
    @app.get("/api/health")
    def health_check():
        return {"success": True, "message": "API operativa."}, 200


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return error_response("Recurso no encontrado.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return error_response("Metodo HTTP no permitido para este recurso.", 405)

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        return error_response("Error interno del servidor.", 500)

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        db.session.rollback()
        app.logger.exception(error)
        return error_response("Ocurrio un error inesperado.", 500)


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=app.config.get("DEBUG", False))
