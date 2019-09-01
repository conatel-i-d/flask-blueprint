import os
from flask import jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, fields

from app.api_flask import ApiFlask
from app.api_exception import ApiException

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    from app.errors import register_error_handlers
    # Creamos la aplicación de Flask
    app = Flask(__name__)
    config = config_by_name[env or "test"]
    app.config.from_object(config)
    # Creacmos el objeto `api`
    api_title = os.environ.get('APP_TITLE', config.TITLE)
    api_version = os.environ.get('APP_VERSION', config.VERSION)
    api = ApiFlask(app, title=api_title, version=api_version)
    # Registramos las rutas
    register_routes(api, app)
    # Registramos loa error_handlers
    register_error_handlers(app)
    # Inicializamos la base de datos
    db.init_app(app)
    # Creamos una ruta para chequear la salud del sistema
    @app.route('/healthz')
    # pylint: disable=unused-variable
    def healthz(): 
        """ Healthz endpoint """
        return jsonify({"ok": True})
    # Retornamos la aplicación de Flask
    return app, api