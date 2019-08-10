from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource
from flask.wrappers import Response
from typing import List

from app.api_response import ApiResponse
from .schema import EntitySchema
from .service import EntityService
from .model import Entity
from .interface import EntityInterface

api = Namespace("Entity", description="Single entity")  # noqa


@api.route("/")
class EntityResource(Resource):
    """
    Entity Resource
    """

    @responds(schema=EntitySchema, many=True, wrapper=ApiResponse)
    def get(self) -> ApiResponse:
        """
        Returns the list of entities
        """
        return ApiResponse(EntityService.get_all())

    @accepts(schema=EntitySchema, api=api)
    @responds(schema=EntitySchema)
    def post(self) -> Entity:
        """
        Create a Single Entity
        """
        #return ApiResponse(EntityService.create(request.parsed_obj), 201)
        return EntityService.create(request.parsed_obj)


@api.route("/<int:id>")
@api.param("id", "Entity database ID")
class EntityIdResource(Resource):
    @responds(schema=EntitySchema)
    def get(self, id: int) -> Entity:
        """Get Single Entity"""

        return EntityService.get_by_id(id)

    def delete(self, id: int) -> Response:
        """Delete Single Entity"""
        from flask import jsonify

        id = EntityService.delete_by_id(id)
        return jsonify(dict(status="Success", id=id))

    @accepts(schema=EntitySchema, api=api)
    @responds(schema=EntitySchema)
    def put(self, id: int):
        """Update Single Entity"""

        changes: EntityInterface = request.parsed_obj
        Entity = EntityService.get_by_id(id)
        return EntityService.update(Entity, changes)