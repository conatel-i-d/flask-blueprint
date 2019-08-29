from marshmallow import fields as marshmallow_fields, Schema
from flask_restplus import fields as restplus_fields

class BaseInterfaces(object):
    """ Base interfaces class """

    def __init__(self):
        self.schema = self.create_marshmallow_schema()

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
        fields = dict()
        for key in fields_keys:
            attributes = getattr(self, key).get('m')
            print(attributes)
            field = getattr(marshmallow_fields, attributes['field'])
            if field is None:
                continue
            fields[key] = field(**attributes)
        return type('MarshmallowSchema', (Schema,), fields)