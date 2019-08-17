from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from typing import List

from app.api_response import ApiResponse
from .schema import EntitySchema
from .service import EntityService
from .model import Entity

api = Namespace('Entity', description="Entity resources")

model_schema = EntitySchema()
collection_schema = EntitySchema(many=True)

base = api.model('EntityBase', {
    'name': fields.String(description='Name of the entity', required=False, example='My entity'),
    'purpose': fields.String(description='Purpose of the entity', required=False, example='The purpose of life is 42'),
})
model = api.inherit('Entity', base, {
    'id': fields.Integer(description='Unique identifier', required=True, example=123),
})
model_response = api.model('EntityResponse', {
    'item': fields.Nested(model)
})
collection = api.model('EntityCollection', {
    'items': api.as_list(fields.Nested(model)),
    'count': fields.Integer
})

@api.route("/")
class EntityResource(Resource):
    """
    Entity Resource
    """

    @api.response(200, 'Entity List', collection)
    def get(self) -> ApiResponse:
        """
        Returns the list of entities
        """
        entities = EntityService.get_all()
        return ApiResponse(collection_schema.dump(entities).data)

    @api.expect(base)
    @api.response(200, 'New Entity', model)
    def post(self) -> Entity:
        """
        Create a single Entity
        """
        body = model_schema.load(request.get_json()).data
        entity = EntityService.create(body)
        return ApiResponse(model_schema.dump(entity).data)


@api.route("/<int:id>")
@api.param("id", "Entity database ID")
class EntityIdResource(Resource):
    @api.response(200, 'Wanted entity', model)
    def get(self, id: int) -> Entity:
        """
        Get a single Entity
        """
        entity = EntityService.get_by_id(id)
        return ApiResponse(model_schema.dump(entity).data)

    @api.response(204, 'No Content', model)
    def delete(self, id: int) -> Response:
        """
        Delete a single Entity
        """
        from flask import jsonify

        id = EntityService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(base)
    @api.response(200, 'Updated Entity', model)
    def put(self, id: int):
        """Update a single Entity"""
        body = model_schema.load(request.json).data
        entity = EntityService.update(id, body)
        return ApiResponse(model_schema.dump(entity).data)