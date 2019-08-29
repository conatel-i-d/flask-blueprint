import inspect
import pytest
from flask_restplus import Namespace

from .base_interfaces import BaseInterfaces, marshmallow_fields, restplus_fields

class ChildInterfaces(BaseInterfaces):
    __name__ = 'Test'
    id = dict(
        m=marshmallow_fields.Int(attribute='id'),
        r=restplus_fields.Integer(description='Unique identifier', required=True, example=123),
    )
    firstName = dict(
        m=marshmallow_fields.String(attribute='first_name'),
        r=restplus_fields.String(description='User first name', required=False, example="Example"),
    )
    admin = dict(
        m=marshmallow_fields.Bool(attribute='admin', default=False, required=True),
        r=restplus_fields.Boolean(description='User is Admin?', required=False, example=False, default=False)
    )
    create_model_keys = ['firstName', 'admin']
    update_model_keys = ['admin']

@pytest.fixture
def api():
    return Namespace('Test', description="Test resources")

@pytest.fixture
def base(api):
    return BaseInterfaces(api)

@pytest.fixture
def child(api):
    return ChildInterfaces(api)

def test_class_existance(base):
    assert base != None

def test_pick_exists(child):
    assert getattr(child, 'pick') != None

def test_pick_returns_list(child):
    actual = child.pick(['admin', 'firstName', 'id'])
    assert len(actual) == 3

def test_create_marshmallow_schema_exists(child):
    assert child.create_marshmallow_schema != None

def test_create_marshmallow_schema_result(child):
    assert inspect.isclass(child._schema) == True

def test_schema_is_valid(child):
    schema = child._schema()
    actual = schema.dump(dict(id='not an int')).data
    assert actual == dict(admin=False)
    actual = schema.dump(dict(id=1)).data
    assert actual == dict(id=1, admin=False)
    actual = schema.dump(dict(id=1, first_name='Example', admin=True)).data
    assert actual == dict(id=1, firstName='Example', admin=True)

def test_single_schema_works(child):
    actual = child.single_schema.dump(dict(id='not an int')).data
    assert actual == dict(admin=False)
    actual = child.single_schema.dump(dict(id=1)).data
    assert actual == dict(id=1, admin=False)
    actual = child.single_schema.dump(dict(id=1, first_name='Example', admin=True)).data
    assert actual == dict(id=1, firstName='Example', admin=True)

def test_many_schema_works(child):
    actual = child.many_schema.dump([dict(id='not an int')]).data
    assert actual == [dict(admin=False)]
    actual = child.many_schema.dump([dict(id=1)]).data
    assert actual == [dict(id=1, admin=False)]
    actual = child.many_schema.dump([dict(id=1, first_name='Example', admin=True)]).data
    assert actual == [dict(id=1, firstName='Example', admin=True)]

def test_create_model_is_valid(child):
    print(child.create_model)
    assert str(child.create_model) == 'Model(TestCreate,{admin,firstName})'

def test_update_model_is_valid(child):
    print(child.update_model)
    assert str(child.update_model) == 'Model(TestUpdate,{admin})'

def test_model_is_valid(child):
    print(child.model)
    assert str(child.model) == 'Model(Test,{admin,firstName,id})'

def test_single_response_model_is_valid(child):
    print(child.single_response_model)
    assert str(child.single_response_model) == 'Model(TestSingleResponse,{item})'

def test_many_response_model_is_valid(child):
    print(child.many_response_model)
    assert str(child.many_response_model) == 'Model(TestManyResponse,{items,count})'