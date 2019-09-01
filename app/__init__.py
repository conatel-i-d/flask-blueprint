import os
from flask import jsonify, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, apidoc

from app.api_flask import ApiFlask

db = SQLAlchemy()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    from app.errors import register_error_handlers
    # Creamos la aplicación de Flask
    app = Flask(__name__, template_folder='./templates')
    config = config_by_name[env or "test"]
    app.config.from_object(config)
    # Creacmos el objeto `api`
    api_title = os.environ.get('APP_TITLE', config.TITLE)
    api_version = os.environ.get('APP_VERSION', config.VERSION)
    api_description = """
    API de ejemplo, para mostrar como se deben construir APIs con `flask`.

    La idea detras de este proyecto es simplificar la construcción de API con `flask`.
    Se incluyen un montón de opiniones sobre como se deben solucionar los problemas
    típicos que surgen cuando se crea una API, como: validación, paginación, autenticación,
    etc.

    Se incluyen ejemplos que muestran como se puede construir la documentación del sitio de forma
    automatica, utilizando `flask_restplus`.

    Por último, se incluyen ejemplos sobre como se pueden construir `tests` sobre los 
    distintos componentes de la `app`. Cuantas más `tests` se incluyan, más manenible
    es el proyecto.
    """
    api = ApiFlask(app, 
        title=api_title, 
        version=api_version, 
        description=api_description,
        license='MIT',
        licence_url='https://opensource.org/licenses/MIT',
        endpoint='',
    )
    # Registramos las rutas
    register_routes(api, app)
    # Registramos loa error_handlers
    register_error_handlers(app)
    # Inicializamos la base de datos
    db.init_app(app)
    # Configuración de página de documentación
    @api.documentation
    # pylint: disable=unused-variable
    def custom_ui():
        return render_template('api_docs.html')
        # return apidoc.ui_for(api)
    # Creamos una ruta para chequear la salud del sistema
    @app.route('/healthz')
    # pylint: disable=unused-variable
    def healthz(): 
        """ Healthz endpoint """
        return jsonify({"ok": True})
    # Retornamos la aplicación de Flask
    return app, api