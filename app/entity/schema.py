from marshmallow import fields, Schema

class EntitySchema(Schema):
    """ Entity marshmallow schema """

    id = fields.Int(attribute='id', dump_only=True)
    name = fields.String(attribute='name')
    purpose = fields.String(attribute='purpose')
    snake_case = fields.String(attribute='camelCase')