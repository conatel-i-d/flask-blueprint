import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    # Creamos la aplicación de Flask
    app = Flask(__name__)
    config = config_by_name[env or "test"]
    app.config.from_object(config)
    # Creacmos el objeto `api`
    api_title = os.environ.get('APP_TITLE', config.TITLE)
    api_version = os.environ.get('APP_VERSION', config.VERSION)
    api = Api(app, title=api_title, version=api_version)
    # Registramos las rutas
    register_routes(api, app)
    # Inicializamos la base de datos
    db.init_app(app)
    # Creamos una ruta para chequear la salud del sistema
    @app.route('/healthz')
    # pylint: disable=unused-variable
    def healthz(): 
        """ Healthz endpoint """
        return jsonify({"ok": True})
    # Retornamos la aplicación de Flask
    return app