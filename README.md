# `flask-blueprint`

Blueprint para la creación de APIs con Flask

## Inspiración

Este proyecto esta fuertemente inspirado por los siguientes recursos:

- [Talk "Flask for Fun and Profit", Armin Ronacher, PyBay2016, YouTube](https://www.youtube.com/watch?v=1ByQhAM5c1I)
  - [Slides deck](https://speakerdeck.com/mitsuhiko/flask-for-fun-and-profit?slide=42)
- [Blog "Flask best practises", AJ Pryor, http://alanpryorjr.com](http://alanpryorjr.com/2019-05-20-flask-api-example/)

## Potenciales problemas

- Utiliza la librería [`flask_accepts`](https://github.com/apryor6/flask_accepts) que tiene pocos usuarios. De todas maneras el codigo es simple, y no debería ser dificil de solucionar en caso de que ocurran bugs. 

## Librerías

- [`flask`](https://palletsprojects.com/p/flask/)
- [`pytest`](https://docs.pytest.org/en/latest/)
- [`marshmallow`](https://marshmallow.readthedocs.io/en/3.0/)
- [`sqlalchemy`](https://www.sqlalchemy.org/)
- [`flask-restplus`](https://flask-restplus.readthedocs.io/en/stable/)
- [`flask_accepts`](https://github.com/apryor6/flask_accepts)

## Notas

### Estructura

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

#### ¿Nombres en singular o plural?

Es importante notar que el nombre de la `entity` esta en singular. Esto es porque todos los lenguajes ya tienen una forma nativa de definir una lista de elementos, como un `array` o una `tupla`. Todos los demás recursos también se nombrarán en singular.

¿Cuando no se seguira esta regla?

Cuando se tenga que nombrar una `entity` en un sistema que no cuente con una abstacción nativa de una lista. Por ejemplo:

- En SQL cuando se quiere referenciar una tabla.
- Al crear las rutas de una `entity`

#### `Model`

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

#### `Interface`

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

#### `Schemas`

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

#### Services

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














































