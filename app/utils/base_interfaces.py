from marshmallow import fields as marshmallow_fields, Schema
from flask_restplus import fields as restplus_fields

class BaseInterfaces(object):
    """ Base interfaces class """
    update_keys = []

    def __init__(self, api, name=''):
        self._api = api
        self.__name__ = getattr(self, '__name__', None) or name
        self._schema = self.create_marshmallow_schema()
        self.single_schema = self._schema()
        self.many_schema = self._schema(many=True)
        self.create_model_keys = getattr(self, 'create_model_keys', None) or self.get_restplus_fields_keys()
        self.create_model = self._api.model(self.__name__ + 'Create', self.get_restplus_fields(self.create_model_keys))
        self.update_model_keys = getattr(self, 'update_model_keys', None) or self.create_model_keys
        self.update_model = self._api.model(self.__name__ + 'Update', self.get_restplus_fields(self.update_model_keys))
        self.model = self._api.model(self.__name__, self.get_restplus_fields(self.get_restplus_fields_keys()))
        self.single_response_model = self.create_single_response_model()
        self.many_response_model = self.create_many_response_model()

    def get_restplus_fields(self, keys):
        return {key: getattr(self, key).get('r') for key in self.get_restplus_fields_keys() if key in keys}

    def get_restplus_fields_keys(self):
        return [field for field in self.attributes() if
            type(getattr(self, field)) is dict
            and getattr(self, field).get('r') is not None
        ]

    def get_marshmallow_fields_keys(self):
        return [field for field in self.attributes() if
            type(getattr(self, field)) is dict
            and getattr(self, field).get('m') is not None
        ]

    def attributes(self):
        return [key for key in dir(self) if 
            not key.startswith('__')
            and not key in ['schema']
            and not callable(getattr(self, key))
        ]

    def pick(self, keys):
        values = [getattr(self, key) for key in self.attributes() if key in keys]
        return values
    
    def create_marshmallow_schema(self):
        fields_keys = self.get_marshmallow_fields_keys()
        return type(self.__name__ + 'MarshmallowSchema', (Schema,), {field_key: getattr(self, field_key).get('m') for field_key in fields_keys})

    def create_single_response_model(self):
        return self._api.model(self.__name__ + 'SingleResponse', dict(
            item=restplus_fields.Nested(self.model),
        ))

    def create_many_response_model(self):
        return self._api.model(self.__name__ + 'ManyResponse', dict(
            items=restplus_fields.List(restplus_fields.Nested(self.model)),
            count=restplus_fields.Integer
        ))