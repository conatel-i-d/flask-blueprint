# `flask-blueprint`

Blueprint para la creación de APIs con Flask

## Indice

- [Inspiración](#inspiration)
- [Consideraciones](#considerations)
- [Librerías](#libraries)
- [Estructura](#structure)
  - [Convención de nombres](#naming_convention)
  - [`Model`](#model)
  - [`Interface`](#interface)
  - [`Schema`](#schema)
  - [`Service`](#service)
  - [`Controller`](#controller)
  - [Declaración de rutas](#route_declaration)
- [`create_app`](#create_app)
- [Fixtures](#fixtures)
- [Run](#run)

## Inspiración<a name="inspiration"></a>

Este proyecto esta fuertemente inspirado por los siguientes recursos:

- [Talk "Flask for Fun and Profit", Armin Ronacher, PyBay2016, YouTube](https://www.youtube.com/watch?v=1ByQhAM5c1I)
  - [Slides deck](https://speakerdeck.com/mitsuhiko/flask-for-fun-and-profit?slide=42)
- [Blog "Flask best practises", AJ Pryor, http://alanpryorjr.com](http://alanpryorjr.com/2019-05-20-flask-api-example/)

## Consideraciones<a name="considerations"></a>

- Utiliza la librería [`flask_accepts`](https://github.com/apryor6/flask_accepts) que tiene pocos usuarios. De todas maneras el codigo es simple, y no debería ser dificil de solucionar en caso de que ocurran bugs. 

## Librerías<a name="library"></a>

- [`flask`](https://palletsprojects.com/p/flask/)
- [`pytest`](https://docs.pytest.org/en/latest/)
- [`marshmallow`](https://marshmallow.readthedocs.io/en/3.0/)
- [`sqlalchemy`](https://www.sqlalchemy.org/)
- [`flask-restplus`](https://flask-restplus.readthedocs.io/en/stable/)
- [`flask_accepts`](https://github.com/apryor6/flask_accepts)
- [`flask_scripts`](https://flask-script.readthedocs.io/en/latest/)

## Estructura<a name="structure"></a>

Todos los archivos que estén relacionados por un mismo topico, deben pertenecer al mismo modulo. No se crean carpetas de `controllers`, `models`, etc.

La unidad básica de una API es un `entity`, que corresponde a "aquello sobre lo que queremos operar". Cada `entity` debe contar con al menos las siguientes piezas:

- `Model`: Representación de Python de la `entity`.
- `Interface`: Define los tipos que conforman la `entity`.
- `Controller`: Orquesta las rutas, servicios y esquemas de la `entity`.
- `Schema`: Serializa y deserializa `entities`.
- `Service`: Manipula `entities`. Por ejemplo, operaciones CRUD.

Los archivos de prueba de cada entidad deben existir en conjunto con los archivos de la aplicación.

La estructura final será similar a la siguiente:

```
/entity
  __init__.py
  controller.py
  controller_test.py
  interface.py
  interface_test.py
  model.py
  model_test.py
  schema.py
  schema_test.py
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

### `Interface`<a name="interface"></a>

_Define los tipos que conforman la `entity`._

La razón de contar con un archivo adicional para definir la `entity` es para separar: _que es_ (`Model`), de _que lo hace_ (`Interface`). La `Interface` permite ser específico en los parámetros que necesito para interactuar (crear, modificar, buscar, elminar, etc.) con una `entity`.

Además, ayudan a escribir la documentación de la `entity`.

Para su definición usaremos un `TypeDict`, que funciona de forma similar que un diccionario convencional de `python` pero que permite definir que variables son aceptadas bajo cada llave. Es por esto que los hace utiles para definir `Interfaces`.

Por ahora no son parte de `python` directamente, debemos obtenerlo de la librería [`mypy_extensions`](https://pypi.org/project/mypy_extensions/). Esta líbrería se define de la siguiente manera:

> The `mypy_extensions` module defines experimental extensions to the standard “typing” module that are supported by the `mypy` typechecker.

Y `mypy` es un motor de tipos opcionales para `python`. Los tipos ayudan a auto-documentar el código y evitan una serie de errores en `runtime`. Su uso no impacta con el funcionamiento del programa.

Los `TypeDict` van a ser agregados formalmente a `python` en la versión `3.8`.

```python
from mypy_extensions import TypedDict

class EntityInterface(TypeDict, total=False):
    id: int
    name: str
```

_Las `Interfaces` y los `Schemas` no tienen por que contar con una suite de pruebas._

### `Schemas`<a name="schemas"></a>

_Serializa y deserializa `entities`._

Utilizaremos `marshmallow` para serializar y deserializar `entities`. En partícular, utilizaremos los `Schemas` para realizar los cambios de nombres correspondientes de nuestras variables. En JSON y JavaScript, se suele utilizar `camelCase` para definir el nombre de las variables, mientras que en Python se usa `snake_case`.

```python
from marshmallow import fields, Schema

class EntitySchema(Schema):
    ''' Entity Schema '''
    id = fields.Number(attribute='id')
    name = fields.String(attribute='name')
    camelCase = fields.string(attribute='snake_case')
```

_Las `Interfaces` y los `Schemas` no tienen por que contar con una suite de pruebas._

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

## `create_app`<a name="create_app"></a>

Para poder testear correctamente la API, necesitamos una forma sencilla de crearla. Un patron utilizado en Flask es crear un metodo llamado `create_app` que cree la API, consumiendo una lista de configuraciones.

Dentro de `app/__init__.py` creamos el siguiente metodo:

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

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
    with client
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






























