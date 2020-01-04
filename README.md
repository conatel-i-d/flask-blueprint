# `flask-blueprint`

Blueprint para la creación de APIs con Flask

## Indice

- [Inspiración](#inspiration)
- [Consideraciones](#considerations)
- [Librerías](#libraries)
- [Estructura](#structure)
  - [Convención de nombres](#naming_convention)
  - [`Model`](#model)
  - [`Interfaces`](#interfaces)
  - [`Service`](#service)
  - [`Controller`](#controller)
  - [Declaración de rutas](#route_declaration)
- [API Response](#api_response)
- [Paginación](#pagination)
- [Orden](#order)
- [Filtros](#filters)
- [Busqueda](#search)
- [Errors](#errors)
- [Authorización](#authorization)
- [`create_app`](#create_app)
- [Fixtures](#fixtures)
- [Run `dev`](#run)
- [Tests](#test)
- [Swagger](#swagger)
- [Migraciones](#migrations)
  - [Uso de `alembic`](#alembic_use)
- [Puesta en producción](#production)
  - [Docker Compose](#production_docker_compose)
  - [Kubernetes](#production_kubernetes)
  - [AWS Lambda](#production_aws_lambda) 

## Inspiración<a name="inspiration"></a>

Este proyecto esta fuertemente inspirado por los siguientes recursos:

- [Talk "Flask for Fun and Profit", Armin Ronacher, PyBay2016, YouTube](https://www.youtube.com/watch?v=1ByQhAM5c1I)
  - [Slides deck](https://speakerdeck.com/mitsuhiko/flask-for-fun-and-profit?slide=42)
- [Blog "Flask best practises", AJ Pryor, http://alanpryorjr.com](http://alanpryorjr.com/2019-05-20-flask-api-example/)

## Librerías<a name="libraries"></a>

- [`flask`](https://palletsprojects.com/p/flask/)
- [`pytest`](https://docs.pytest.org/en/latest/)
- [`marshmallow`](https://marshmallow.readthedocs.io/en/3.0/)
- [`sqlalchemy`](https://www.sqlalchemy.org/)
- [`flask-restplus`](https://flask-restplus.readthedocs.io/en/stable/)
- [`alembic`](https://alembic.sqlalchemy.org)

## Estructura<a name="structure"></a>

Todos los archivos que estén relacionados por un mismo topico, deben pertenecer al mismo modulo. No se crean carpetas de `controllers`, `models`, etc.

La unidad básica de una API es un `entity`, que corresponde a "aquello sobre lo que queremos operar". Cada `entity` debe contar con al menos las siguientes piezas:

- `Model`: Representación de Python de la `entity`.
- `Controller`: Orquesta las rutas, servicios y esquemas de la `entity`.
- `Interfaces`: Serializa y deserializa los menajes para manipular las `entities`. También sirve para documentar las interfaces.
- `Service`: Manipula `entities`. Por ejemplo, operaciones CRUD.

Los archivos de prueba de cada entidad deben existir en conjunto con los archivos de la aplicación.

La estructura final será similar a la siguiente:

```
/entity
  __init__.py
  controller.py
  controller_test.py
  model.py
  model_test.py
  interfaces.py
  service.py
  service_test.py
```

### Convención de nombres<a name="naming_convention"></a>

Es importante notar que el nombre de la `entity` esta en singular. Esto es porque todos los lenguajes ya tienen una forma nativa de definir una lista de elementos, como un `array` o una `tupla`. Todos los demás recursos también se nombrarán en singular.

¿Cuando no se seguira esta regla?

Cuando se tenga que nombrar una `entity` en un sistema que no cuente con una abstacción nativa de una lista. Por ejemplo:

- En SQL cuando se quiere referenciar una tabla.
- Al crear las rutas de una `entity`

### `Model`<a name="model"></a>

_Representación de Python de la `entity`._

Usualmente será una clase basada en `db.Model` de `sqlalchemy`. Sin embargo, este no tiene que ser el único caso.

```python
class Entity(db.Model):
    """ Modelo de la entidad `Entity`. """
    __tablename__ = 'entities'
    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
```

Como mínmo, se debe hacer un `fixture` para probar la existencia del modelo.

```python
from pytest import fixture
from .model import Entity

@fixture
def entity() -> Entity:
    return Entity(
      id=1, name="Test Entitity"
    )
    
def test_Entity_create(entity: Entity):
    assert entity
```

### `Interfaces`<a name="interfaces"></a>

_Serializa y deserializa los menajes para manipular las `entities`. También sirve para documentar las interfaces._

Utilizaremos `marshmallow` para serializar y deserializar `entities`. En partícular, utilizaremos el objeto `Interfaces` para realizar los cambios de nombres correspondientes de nuestras variables. En JSON y JavaScript, se suele utilizar `camelCase` para definir el nombre de las variables, mientras que en Python se usa `snake_case`.

```python
from app.utils.base_interfaces_test import BaseInterfaces, marshmallow_fields, restplus_fields

class EntityInterfaces(BaseInterfaces):
    ''' Entity Schema '''
    __name__ = 'Entity'
    id = dict(
        m=marshmallow_fields.Int(attribute='id', dump_only=True),
        r=restplus_fields.Integer(description='Unique identifier', required=True, example=123),
    )
    name = dict(
        m=marshmallow_fields.String(attribute='name'),
        r=restplus_fields.String(description='Name of the entity', required=False, example='My entity'),
    )
    camelCase = dict(
        m=marshmallow_fields.String(attribute='snake_case'),
        r=restplus_fields.String(
            description='Example of how to convert from camelCase to snake_case',
            required=False,
            example='Something'    
        )
    )
    create_model_keys = ['name', 'camelCase']
    update_model_keys = ['camelCase']
```

El objeto `Interfaces` hereda de la clase `BaseInterfaces`, creada a medida para este proyecto. La dificultad que intenta suplir, es el de tener que montar los esquemas de `marshmallow` y los modelos de `flask-restful`, para manipular los mensajes JSON, y documentar las interfaces.

Esta clase espera que se le configuren todos los atributos, con sus configuraciones de `marshmallow` y `flask-restful`, identificados dentro de un diccionario bajo las llaves `m`, y `r` respectivamente. Luego al momento de crear una instancia de esta clase, quedarán disponibles distintos modelos y esquemas para simplificar la serialización/deserialización de los datos, y simplificar su documentación.

A continuación se presenta la definicón de dicha clase, y los atributos disponibles:

```txt
This class simplifies the creation of `marshmallo` schemas, and 
`flask_restplus` models to document the API.

Args:
    api (flask_restplus.Namespace): `flask_restplus` Namespace instance.
    name (str, optional): Name of the entity.

Attributes:
    _api (flask_restplus.Namespace): `flask_restplus` Namespace instance.
    __name__ (string): Name of the entity. Used as prefix for the model names.
    _shcema (marshmallow.Schema): Dynamically generated `marshmallow` :class:`Schema`.
    single_schema (marshmallow.Schema): `marshmallow` instance for a single entity.
    many_shcema (marshmallow.Schema): `marshmallow` instance for a list of entities.
    create_model_keys (:list:str): List of field names that creates the entity's create model.
    update_model_keys (:list:str): List of field names that creates the entity's update model.
    create_model (flask_restplus.Namespace.model): Entity's create model.
    update_model (flask_restplus.Namespace.model): Entity's update model.
    model (flask_resplus.Namespace.model): Entity's model.
    single_response_model (flask_restplus.Namespace.model): Single entity's response model.
    many_response_model (flask_restplus.Namespace.model): Multiple entity's response model.
```

_Las `Interfaces` no tienen por que contar con una suite de pruebas._

### Services<a name="services"></a>

_Manipula `entities`. Por ejemplo, operaciones CRUD._

Otras funciones de las cuales estan encargados los `Services` son:

- Obtener información de una API.
- Manipular data frames.
- Obtener predicciones a partir de modelos de ML.
- Etc.

Deben estar encargados de todas las tareas relacionadas con el procesamiento de datos. Los servicios pueden depender de otros servicios. No así los `Models`. Esta es una distinción importante.

```python
from app import db
from typing import List

from .model import Entity
from .interface import EntityInterface


class EntityService():
    @classmethod
    def get_all() -> List[Entity]:
        return Entity.query.all()
        
    @statimethod
    def get_by_id(id: int) -> Entity:
        return Entity.query.get(id)
        
    @staticmethod
    def update(id: int, attributes: EntityInterface) -> Entity:
        entity = Entity.query.get(id)
        entity.update(updates)
        db.session.commit()
        return entity
        
    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        entity = Entity.query.filter(Entity.id == id).fist()
        if not entity:
            return []
        db.session.delete(entity)
        db.session.commit()
        return [id]
        
    @staticmethod
    def create(attributes: EntityInterface) -> Entity:
        entity = Entity(name=attributes['name'])
        db.session.add(entity)
        db.session.commit()
        return entity
```

Los `Services` deben contar con pruebas sobre todos sus metodos. Como interactuan con otros servicios usualmente es necesario realizar `mocks` de los mismos.

```python
from flas_sqlalchemy import SQLAlchemy
from typing import List

from app.test.fixtures import app, db # noqa
from .model import Entity
from .service import EntityService
from .interface import EntityInterface


def test_get_all(db: SQLAlchemy): # noqa
    entity_1 = Entity(id=1, name='1')
    entity_2 = Entity(id=2, name='2')
    db.session.add(entity_1)
    db.session.add(entity_2)
    db.session.commit()
    results: List[Entity] = EntityService.get_all()
    assert len(results) == 2
    assert entity_1 in results and entity_2 in results
    
def test_update(db: SQLAlchemy): #noqa
    id = 1
    entity: Entity = Entity(id=id, name='1')
    db.session.add(entity_1)
    db.session.commit()
    attributes: EntityInterface = {'name': '2'}
    EntityService.update(1, updates)
    result: Entity = Entity.query.get(id)
    assert result.name == '2'
    
def test_delete_by_id(db: SQLAlchemy): #noqa
    entity_1 = Entity(id=1, name='1')
    entity_2 = Entity(id=2, name='2')
    db.session.add(entity_1)
    db.session.add(entity_2)
    db.session.commit()
    EntityService.delete_by_id(1)
    db.session.commit()
    results: List[Entity] = Entity.query.all()
    assert len(results) == 1
    assert entity_1 not in results and entity_2 in results
    
def test_create(db: SQLAlchemy): # noqa
    attributes: EntityInterface = {'name': '1'}
    EntityService.create(attributes)
    results: List[Entity] = Widget.query.all()
    assert len(results) == 1
    for key in attributes.keys():
        assert getattr(results[0], key) == attributes[key]
```

Para simplificar la creación de los `services` se creo una clase base llamada `BaseService`
que integra la mayoría de casos típicos necesarios. Para crear un nuevo servicio con ella, 
solo es necesario extenderla, y configurar el `model` y sus `interfaces`.

```python
from app.utils.base_service import BaseService
from .model import Entity
from .interfaces import EntityInterfaces


class EntityService(BaseService):
    model = Entity
    interfaces = EntityInterfaces
```

### Controller<a name="controller"></a>

_Orquesta las rutas, servicios y esquemas de la `entity`._

Además, podemos utilizar `flask-restplus` para documentar la API con Swagger.

```python
from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import EntitiySchema
from .service import EntityService
from .model import Entity
from .interface import EntityInterface

api = Namespace('Entity', description='Single namespace, single entity')


@api.route('/')
class EntityResource(Resource):
    """ Entity Resource """
    
    @responds(schema=EntitySchema, many=True)
    def get(self) -> List[Entity]:
        """ Get all entities """
        return EntityService.get_all()
        
    @accepts(schema=EntitySchema, api=api)
    @responds(schema=EntitySchema)
    def post(self) -> Entity:
        """ Create a single Entity """
        return EntityService.create(request.parsed_obj)
        
@api.route('/<int:id>')
@api.param('id', 'Entity ID')
class EntityIdResource(Resource):
    """ Entity ID Resource """
    
    @responds(schema=EntitySchema)
    def get(self, id: int) -> Entity:
        """ Get a single Entity """
        return EntityService.get_by_id(id)
        
    def delete(self, id: int) -> Response:
        """ Delete a single Entity """
        from flask import jsonify
        id = WidgetService.delete_by_id(id)
        return jsonify({ 'status: 'success', 'id': id })
        
    @accepts(schema=EntitySchema, api=api)
    @responds(schema=EntitySchema)
    def put(self, id: int) -> Entity:
        """ Update a single Entity """
        return EntityService.update(id, request.parsed_obj)
```

> `request.parsed_object` es creado por el docorador `accepts` de `flask_accepts`. El mismo consume el esquema, y se encarga de deserializar el cuerpo para convertirlo a un diccionario valido que podemos usar luego en nuestros `Services`.

Para testear los controladores tendremos que construir un `mock` del `Service`. Esto es para mantener las priebas del `Controller` aisladas del `Service`.

```python
from unittest.mock import patch
from flask.testing import FlaskClient

from app.test.fixtures import client, app # noqa
from .service import EntityService
from .schema import EntitySchema
from .model import Entity
from .interface import EntityInterface
from . import BASE_ROUTE

def make_entity(id: int = 123, name: str = 'Test Entity') -> Entity:
    return Entity(id=id, name=name)
    
class TestEntityResource:
    @patch.object(EntityService, 'get_all',
                  lambda: [make_entity(123, name='Test Entity 1'),
                           make_entity(124, name='Test Entity 2')])
    def test_get(self, client: FlaskClient): #noqa
        with client:
            results = client.get(f'/api/{BASE_ROUTE}', follow_redirects=True).get_json()
            expected = EntitySchema(many=True).dump(
                [make_entity(123, name='Test Entity 1'),
                 make_entity(124, name='Test Entity 2')]
            ).data
            for r in results:
                assert r in expected
```

### Declaración de rutas <a name="route_declaration"></a>

Lo último que queda definir es como se terminan registrando las rutas en la API. La siguiente forma muestra como hacerlo evitando problemas de importaciones circulares.

Definimos dentro de cada carpeta de entidad la configuración de las rutas en el archivo `./app/entity/__init__.py`.

```python
from .model import Entity #noqa
from .schema import WidgetSchema # noqa

BASE_ROUTE = 'entity'

def register_routes(api, app, root='api'):
    """ Registramos las rutas definidas en la `api` del `Controller` """
    from .controller import api as entity_api
    api.add_namespace(entity_api, path=f'/{root}/{BASE_ROUTE}')
```

Desde otro archivo importaremos esta función, y la llamaremos con el objeto `api` y la aplicación de Flask global.

## API Response<a name="api_response"></a>

Para simplificar la creación del cuerpo de la respuesta, se utilizara una clase llamada `ApiResponse` que deberá ser retornada por los metodos de los `Controllers`. La clase recibira el valor de la respuesta, y el codigo de respuesta. La misma creara luego, internamente, la estructura acorde para la respuesta.

Esto simplificara las tareas de agregar links para la paginación, y para agregar relaciones entre entidades de forma centralizada.

**¿Como hacemos para que `flask` pueda procesar esta clase?**

Sobrescribiendo el método `make_response` de `flask`. Este metodo es llamado previo a la construcción de la respuesta final hacia el cliente. Para poder sobrescribirlo, debemos crear una nueva clase que herede de `flask_restplus.Api`.

```python
from flask_restplus import Api

from app.api_response import ApiResponse


class ApiFlask(Api):
    def make_response(self, rv, *args, **kwargs):
        if isinstance(rv, ApiResponse):
            return rv.to_response()
        return Api.make_response(self, rv, *args, **kwargs)
```

Luego, utilizaremos esta clase para crear nuestra aplicación de `flask`.

## Paginación<a name="pagination"></a>

Para manejar la paginación de los recursos, es necesario configurar los
`services` para que utilicen la función `paginate` de `flask_sqlalchemy.query`.
Esta función espera recibir una página y la cantidad de elementos por página.
Los mismos se configuran ingresando las variables `page` y `per_page`. 

Por defecto, dentro del archivo de configuración de la aplicació se pueden
encontrar los valores por defecto para estas opciones.

Para modificar las mismas es necesario pasar `query parameters` junto con la
consulta. Por ejemplo, un request a la siguiente url:

```
https://api/entity/?page=2&per_page=30
```

Hará que se devuelvan los resultados de la segunda página, la cual contendrá un
máximo de 30 elementos.

Para simplificar el parseo de estos parámetros, se creo un decorador que se
encarga de esto. El mismo se llama `parse_query_parameters` y se encuentra
dentro de `app.utils.decorators`.

```python
@api.response(200, 'Entity List', interfaces.many_response_model)
@parse_query_parameters
  def get(self) -> ApiResponse:
    """
    Returns the list of entities
    """
    entities = EntityService.get_all()
    return ApiResponse(interfaces.many_schema.dump(entities).data)
```

El valor de `per_page` puede ser configurado en cualquier valor por que existe
una variable adicional llamada `max_per_page` que límita de forma general la
cantidad máxima de elementos que se devolverán en cada llamada. Por ahora, no
hay forma de modificar este valor en `runtime`. Solamente se encuentra
configurado como un valor estatico dentro de la configuración de la aplicación.

## Orden<a name="order"></a>

Para manejar el órden de los resultados se utiliza la función `order_by` the
SQLAlchemy. Se puede indicar a través de que columna ordenar los datos
configurando el parámetro `order_by` de la consulta.

Por ejemplo:

```
https://api/entity/?order_by=name
```

La dirección se configura de forma similar utilizando el parámetro `order_dir`.
Por defecto el valor de este parámetro es `asc`. Si se configura como `desc` se
ordenerán los resultados de forma descendiente.

```
https://api/entity/?order_by=name&order_dir=desc
```

Estos parámetros son configurados automaticamente en una ruta configurando el
decorador `parse_query_parameters`.

## Filtros<a name="filters"></a>

TODO

## Busqueda<a name="search"></a>

TODO

## Autorización<a name="authorization"></a>

Para asegurar rutas, lo único que hay que hacer es agregar el decorador `authorize`
al método encargado de manejar esta ruta. El decorador puede encontrarse en
`app.utils.authorize`.

```python
# ...
from app.utils.authorize import authorize
# ...

class EntityIdResource(Resource):
    @api.response(200, 'Wanted entity', interfaces.single_response_model)
    @authorize
    def get(self, id: int) -> Entity:
        """
        Get a single Entity
        """
        entity = EntityService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(entity).data)
```

Solo se podrá llamar al recurso administrado por la función anterior, si el
`request` cuenta con un `jwt` valido dentro del Header `Token`. Sin el mismo
no se podrá acceder a este recurso.

## Errors<a name="errors"></a>

Para los errores podemos hacer algo parecido. Los errores pueden contar con logica compartida, mismos codigos de error, o una misma estructura. Para simplificar como se emiten estos errores, los mismos se tirarán utilizando una clase especial llamada `ApiException`.

```python
from werkzeug.exceptions import HTTPException

from app.api_response import ApiResponse

class ApiException(HTTPException):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code

    def to_response(self):
        return ApiResponse({'message': self.message}, status=self.code)
```

Lo que queda es indicarle a `flask` como reaccionar cunado se enfrenta con una excepción. Para eso utilizamos la función `register_error_handlers`.

```python
def register_error_handlers(app):
    app.register_error_handler(ApiException, lambda err: err.to_response())
```

Cuando `flask` detecte un error de tipo `ApiException`, correrá el código indicado en la función Lambda.

**¿Como lo utilizamos?**

```python
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response

from app.api_response import ApiResponse
from app.api_exception import ApiException

api = Namespace('Math', description="Math resources")

@api.route("/sum")
class MathResource(Resource):
    """Math sum resource"""

    @api.response(200, 'Sum result')
    def get(self) -> ApiResponse:
        """Returns the sim result"""
        a = request.args('a', type=int)
        b = request.args('b', type=int)
        if a is None or b is None:
            raise ApiException('Numbers must be integers')
        return ApiResult({'result': a + b})     
```

## `create_app`<a name="create_app"></a>

Para poder testear correctamente la API, necesitamos una forma sencilla de crearla. Un patron utilizado en Flask es crear un metodo llamado `create_app` que cree la API, consumiendo una lista de configuraciones.

Dentro de `app/__init__.py` creamos el siguiente metodo:

```python
from flask import Flask
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
    api_title = os.environ['APP_TITLE'] or config.TITLE
    api_version = os.environ('APP_VERSION') or config.VERSION
    api = Api(app, title=api_title, version=api_version)
    # Registramos las rutas
    register_routes(api, app)
    # Inicializamos la base de datos
    db.init_app(app)
    # Creamos una ruta para chequear la salud del sistema
    @app.route('/healthz')
    def healthz():
        """ Healthz endpoint """
        return "ok"
    # Retornamos la aplicación de Flask
    return app
```

En `./app/config.py` creamos los archivos de configuración para cada uno de nuestros ambientes (por lo menos `test` y `prod`).

```python
import os

basedir = os.path.abspath(path.dirname(__file__))

class BaseConfig:
    TITLE = 'Api'
    VERSION = '0.0.1'
    CONFIG_NAME = 'base'
    DEBUG = False
    TESTING = False
   
class DevelopmentConfig(BaseConfig):
    CONFIG_NAME: 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/app-dev.db'.format(basedir)
    
class TestingConfig(BaseConfig):
    CONFIG_NAME = 'test'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/app-tetst.db'.format(basedir)
    
class ProductionConfig(BaseConfig):
    CONFIG_NAME = 'prod'
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/app-prod.db".format(basedir)
    
EXPORT_CONFIGS = [
  DevelopmentConfig,
  TestingConfig,
  ProductionConfig,
]

config_by_name = { cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS }
```

Lo único que queda definir es el metodo para importar las rutas `register_routes`, definido en el módulo `./app/routes.py`.

```python
def register_routes(api, app, root="api"):
    # Importamos el metodo `register_routes` de cada `entity` y lo renombramos
    from app.entity import register_routes as attach_entity
    # Registramos las rutas
    attach_entity(api, app)
```

Una de las ventajas del metodo `create_app` es que tambien podemos realizar pruebas sobre el.

```python
from app.test.fixtures import app, client # noqa


def test_app_creates(app): # noqa
    assert app
    
def test_app_healthy(app, client): # noqa
    with client:
        resp = client.get('/healthz')
        assert resp.status_code == 200
        assert resp.text == 'ok'
```

## Fixtures<a name="fixtures"></a>

Los `fixtures` existen para crear un ambiente base confiable y replicable por sobre el cual correr las pruebas. Los metodos de pruebas pueden recibir estos `fixtures` como argumentos al momento de ser llamados. Los mismos se registran utilizando el decorador `@pytset.fixture`. Por ejemplo, para nuestro caso conviene crear un `fixture` para la `app` y uno para la `db`:

```python
import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app('test')

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    from app import db
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
```

Si los definimos en un módulo llamado `test`, despues solo tenemos que importarlos a nuestro archivo de pruebas, y utilizar los mismos nombres de los argumentos, que los utilizados al momento de construir el `fixture`. Si vemos el ejemplo del archivo de pruebas de `create_app` podemos ver como utilizarlos.

## Run `dev`<a name="run"></a>

Para correr la aplicación en modo desarrollo utilizamos el siguiente comando:

```bash
FLASK_ENV=development flask run --port 8000
```

## Tests<a name="tests"></a>

Para correr las pruebas utilizaremos `pytest`. Desde la `cli` solo es necesario utilizar este comando:

```
pytest
```

Flask provee una forma de testear la aplicación, al exponer la clase `Client` de `Werkzeug`, y manejando el contexto local por nosotros.

Lo más importante es contar con un `fixture` que represente al cliente.

En nuestro caso lo definimos de la siguiente manera.

```python
import pytest

from app import create_app
from app.api_flask import ApiFlask

@pytest.fixture
def app():
    return create_app('test')[0]

@pytest.fixture
def client(app):
    return app.test_client()
```

Ahora que contamos con el fixture, lo podemos utilizar dentro de nuestras pruebas.

```python
def test_empty_db(client):
    """Start with a blank database."""
    
    rv = client.get('/')
    assert b'No enties here so far' in rv.data
```

Para probar `POST` requests, podemos pasarle el cuerpo en el argumento `json` del metodo `client.post()`.

```python
def test_messages(client):
    """Tests that messages work."""

    rv = client.post('/add', json=dict(name='Something', purpose='awesome'))
    assert b'{"name": "something", "purpose": "awesome", "id": 1}' in rv
```

Si necesitamos realizar pruebas en base a información recibida en el contexto `request`, `g`, y `session`, podemos utilizar el metodo `test_request_context`, que se encuentra dentro del objeto `app`. El objeto `app` también lo definimos como un `fixture`.

```python
def test_query_parameters(app, client):
    """Test the name in the query parameters."""

    with app.test_request_context('?name=John'):
        assert flask.request.path == '/'
        assert flask.request.args['name'] == 'John'
```

## Swagger<a name=swagger></a>

Al utilizar `flask_restful` ya contamos con documentación en formato `swagger` que podemos visualizar desde la raiz de nuestra API. Osea, si servimos la `api` desde el puerto `8000`, podemos encontrar la documentación en `http://localhost:8000`.

También podemos servir la el documento `swagger` en JSON agregando la siguiente ruta:

```python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource, fields

db = SQLAlchemy()


def create_app(env=None):
    # Dentro de `create_app` despues de definir la `api`
    @app.route('/swagger')
    def swagger():
        """ Swagger JSON docs """
        return jsonify(api.__schema__)
    # ...
```

## Migraciones <a name="migrations"></a>

Las migraciones de la base de datos las haremos con [`alembic`](https://alembic.sqlalchemy.org)

Es una herramienta para desarrollar migraciones de bases de datos desarrollado por el autor de SQLAlchemy. Con esta herramienta podremos:

1. Emitir modificaciones en la base de datos.
2. Construir `scripts` que indiquen una serie de `pasos` necesarios para actualizar o revertir el estado de una tabla.
3. Permite la ejecución de `scripts` de forma secuencial.

### Uso de `alembic`<a name="alembic_use"></a>

Una vez instalado `alembic` debemos crear la carpeta donde se incluiran todas las migraciones. Esto lo hacemos con el comando:

```
alembic init migrations
```

Se creara:

1. Un archivo en la raiz llamado `alembic.ini`
2. Una carpeta llamada `migrations` donde incluiremos nuestros `scripts`.

Dentro del archivo `alembic.ini` colocamos la ruta hacia la base de datos de `dev` modificando el valor de `sqlalchemy.url`.

Las migraciones se crean dentro de revisiones. `Alembic` puede generar los archivos de revisiones por nosotros con el siguiente comando:

```
alembic revision -m "create entity table"
```

El resultado será un nuevo archivo de migración dentro de `./migrations/versions/`. Dentro de este documento tendremos que modificar las declaraciones de las funciones `upgrade()` y `downgrade()`. Las mismas son ejecutadas cuando nos movemos en un, u otro sentido de las migraciones.

El siguiente es un ejemplo de como las podemos configurar para crear una nueva tabla:

```python
def upgrade():
    op.create_table(
        'entity',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('purpose', sa.String(255), nullable=False),
    )

def downgrade():
    op.drop_table('entity')
```

Al finalizar, podemos aplicar nuestra nueva revisión con el comando:

```
alembic upgrade head
```

Esto aplicara todos los cambios definidos en la migración.

Existen otros comandos útiles que `alembic` nos provee:

- Para ver la migración actual
    ```
    alembic current --verbose
    ```
- Para ver la historia de las migraciones
    ```
    alembic history --verbose
    ```
- Para bajar a la versión anterior de la base
    ```
    alembic downgrade -1
    ```
- Para subir a la versión siguiente
    ```
    alembic upgrade +1
    ```
- Para hacer un roll-back de todas las migraciones
    ```
    alembic downgrade base
    ```

## Puesta en producción<a name="production"></a>
  
TODO

### Docker Compose <a name="production_docker_compose"></a>

TODO

### Kubernetes <a name="production_kubernetes"></a>

TODO

### AWS Lambda <a name="production_aws_lambda"></a>

TODO



















