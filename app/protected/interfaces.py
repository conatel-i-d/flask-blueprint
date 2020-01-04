from app.utils.base_interfaces_test import BaseInterfaces, marshmallow_fields, restplus_fields

class ProtectedEntityInterfaces(BaseInterfaces):
    __name__ = 'ProtectedEntity'
    id = dict(
        m=marshmallow_fields.Int(attribute='id', dump_only=True),
        r=restplus_fields.Integer(description='Unique identifier', required=True, example=123),
    )
    name = dict(
        m=marshmallow_fields.String(attribute='name'),
        r=restplus_fields.String(description='Name of the entity', required=False, example='My entity'),
    )
    purpose = dict(
        m=marshmallow_fields.String(attribute='purpose'),
        r=restplus_fields.String(description='Purpose of the entity', required=False, example='The purpose of life is 42'),
    )
    camelCase = dict(
        m=marshmallow_fields.String(attribute='snake_case'),
        r=restplus_fields.String(
            description='Example of how to convert from camelCase to snake_case',
            required=False,
            example='Something'    
        )
    )
    create_model_keys = ['name', 'purpose', 'camelCase']
    update_model_keys = ['purpose', 'camelCase']