"""
Instancias unicas (singletons) de las extensiones de Flask.

Se definen aqui para evitar importaciones circulares entre app.py,
los modelos y las rutas.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
