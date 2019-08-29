from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource, fields
from flask.wrappers import Response
from typing import List

from app.api_response import ApiResponse
from .service import EntityService
from .model import Entity
from .interfaces import EntityInterfaces

api = Namespace('Entity', description="Entity resources")
interfaces = EntityInterfaces(api)

@api.route("/")
class EntityResource(Resource):
    """
    Entity Resource
    """

    @api.response(200, 'Entity List', interfaces.many_response_model)
    def get(self) -> ApiResponse:
        """
        Returns the list of entities
        """
        entities = EntityService.get_all()
        print('entities[0]["snake_case"] =' , getattr(entities[0], 'snake_case'))
        print(interfaces.many_schema)
        return ApiResponse(interfaces.many_schema.dump(entities).data)

    @api.expect(interfaces.create_model)
    @api.response(200, 'New Entity', interfaces.single_response_model)
    def post(self) -> Entity:
        """
        Create a single Entity
        """
        json_data = request.get_json()
        if json_data is None:
            raise Exception('JSON body is undefined')
        body = interfaces.single_schema.load(json_data).data
        print(json_data)
        entity = EntityService.create(body)
        return ApiResponse(interfaces.single_schema.dump(entity).data)


@api.route("/<int:id>")
@api.param("id", "Entity unique identifier")
class EntityIdResource(Resource):
    @api.response(200, 'Wanted entity', interfaces.single_response_model)
    def get(self, id: int) -> Entity:
        """
        Get a single Entity
        """
        entity = EntityService.get_by_id(id)
        return ApiResponse(interfaces.single_schema.dump(entity).data)

    @api.response(204, 'No Content')
    def delete(self, id: int) -> Response:
        """
        Delete a single Entity
        """
        from flask import jsonify

        id = EntityService.delete_by_id(id)
        return ApiResponse(None, 204)

    @api.expect(interfaces.update_model)
    @api.response(200, 'Updated Entity', interfaces.single_response_model)
    def put(self, id: int):
        """Update a single Entity"""
        body = interfaces.single_schema.load(request.json).data
        entity = EntityService.update(id, body)
        return ApiResponse(interfaces.single_schema.dump(entity).data)