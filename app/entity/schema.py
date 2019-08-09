from marshmallow import fields, Schema


class EntitySchema(Schema):
    """Entity schema"""

    id = fields.Number(attribute="id")
    name = fields.String(attribute="name")
    purpose = fields.String(attribute="purpose")