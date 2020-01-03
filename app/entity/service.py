from typing import List

from app import db
from app.utils.query import Query
from .model import Entity


class EntityService:
    @staticmethod
    def get_all() -> List[Entity]:
        """
        Returns all the entities paginated
        """
        return Entity.query.paginate(
            page=Query.get_param('page'),
            per_page=Query.get_param('per_page'),
            error_out=False,
            max_per_page=Query.get_param('max_per_page')
        ).items

    @staticmethod
    def get_by_id(id: int) -> Entity:
        return Entity.query.get(id)

    @staticmethod
    def update(id: int, body) -> Entity:
        entity = EntityService.get_by_id(id)
        if entity is None:
            return None
        entity.update(body)
        db.session.commit()
        return entity

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        entity = Entity.query.filter(Entity.id == id).first()
        if not entity:
            return []
        db.session.delete(entity)
        db.session.commit()
        return [id]

    @staticmethod
    def create(new_attrs) -> Entity:
        new_entity = Entity(name=new_attrs["name"], purpose=new_attrs["purpose"])
        db.session.add(new_entity)
        db.session.commit()
        return new_entity
