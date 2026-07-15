"""
Registro centralizado de todos los Blueprints de la aplicacion.
"""
from routes.auth_routes import auth_bp
from routes.aseguradora_routes import aseguradora_bp
from routes.juzgado_routes import juzgado_bp
from routes.marca_routes import marca_bp
from routes.modelo_routes import modelo_bp
from routes.usuario_routes import usuario_bp
from routes.vehiculo_routes import vehiculo_bp
from routes.expediente_routes import expediente_bp


def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(aseguradora_bp)
    app.register_blueprint(juzgado_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(modelo_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(vehiculo_bp)
    app.register_blueprint(expediente_bp)
