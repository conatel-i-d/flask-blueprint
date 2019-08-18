from flask_restplus import fields

from .schema import EntitySchema

class EntityInterfaces(object):
    """Entity REST+ interfaces"""
    
    """Flask REST+ fields definitions"""
    fields = dict(
        id=fields.Integer(description='Unique identifier', required=True, example=123),
        name=fields.String(description='Name of the entity', required=False, example='My entity'),
        purpose=fields.String(description='Purpose of the entity', required=False, example='The purpose of life is 42'),
    )

    def __init__(self, api):
        self.api = api
        self.create = self.api.model('EntityCreate', self.pick_fields(['name', 'purpose']))
        self.update = self.api.model('EntityUpdate', self.pick_fields(['name', 'purpose']))
        self.model = self.api.model('EntityModel', self.fields)
        self.single = self.create_single_response()
        self.many = self.create_many_response()

    def pick_fields(self, keys):
        return {key: self.fields[key] for key in keys}

    def create_single_response(self):
        return self.api.model('EntitySingleResponse', dict(
            item=fields.Nested(self.model),
        ))

    def create_many_response(self):
        return self.api.model('EntityManyResponse', dict(
            items=fields.List(fields.Nested(self.model)),
            count=fields.Integer
        ))