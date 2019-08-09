from flask import request
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource
from flask.wrappers import Response
from typing import List

from .schema import EntitySchema
from .service import EntityService
from .model import Entity
from .interface import EntityInterface

api = Namespace("Entity", description="Single namespace, single entity")  # noqa


@api.route("/")
class EntityResource(Resource):
    """Entitys"""

    @responds(schema=EntitySchema, many=True)
    def get(self) -> List[Entity]:
        """Get all Entitys"""

        return EntityService.get_all()

    @accepts(schema=EntitySchema, api=api)
    @responds(schema=EntitySchema)
    def post(self) -> Entity:
        """Create a Single Entity"""

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
    def put(self, id: int) -> Entity:
        """Update Single Entity"""

        changes: EntityInterface = request.parsed_obj
        Entity = EntityService.get_by_id(id)
        return EntityService.update(Entity, changes)