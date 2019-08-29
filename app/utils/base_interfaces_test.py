import inspect
import pytest
from marshmallow import exceptions

from .base_interfaces import BaseInterfaces, marshmallow_fields

class ChildInterfaces(BaseInterfaces):
    id = dict(m=marshmallow_fields.Int(attribute='id'))
    first_name = dict(m=marshmallow_fields.String(attribute='firstName'))
    admin = dict(m=marshmallow_fields.Bool(attribute='admin'))

@pytest.fixture
def base():
    return BaseInterfaces()

@pytest.fixture
def child():
    return ChildInterfaces()

def test_class_existance(base):
    assert base != None

def test_pick_exists(child):
    assert getattr(child, 'pick') != None

def test_pick_returns_list(child):
    actual = child.pick(['admin', 'first_name', 'id'])
    assert len(actual) == 3

def test_create_marshmallow_schema_exists(child):
    assert child.create_marshmallow_schema != None

def test_create_marshmallow_schema_result(child):
    assert inspect.isclass(child._schema) == True

def test_schema_is_valid(child):
    schema = child._schema()
    actual = schema.dump(dict(id='not an int')).data
    assert actual == dict()
    actual = schema.dump(dict(id=1)).data
    assert actual == dict(id=1)
    actual = schema.dump(dict(id=1, firstName='Example', admin=False)).data
    assert actual == dict(id=1, first_name='Example', admin=False)

def test_single_schema_works(child):
    actual = child.single_schema.dump(dict(id='not an int')).data
    assert actual == dict()
    actual = child.single_schema.dump(dict(id=1)).data
    assert actual == dict(id=1)
    actual = child.single_schema.dump(dict(id=1, firstName='Example', admin=False)).data
    assert actual == dict(id=1, first_name='Example', admin=False)

def test_many_schema_works(child):
    actual = child.many_schema.dump([dict(id='not an int')]).data
    assert actual == [dict()]
    actual = child.many_schema.dump([dict(id=1)]).data
    assert actual == [dict(id=1)]
    actual = child.many_schema.dump([dict(id=1, firstName='Example', admin=False)]).data
    assert actual == [dict(id=1, first_name='Example', admin=False)]