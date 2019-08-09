from app import db
from typing import List
from .model import Entity
from .interface import EntityInterface


class EntityService:
    @staticmethod
    def get_all() -> List[Entity]:
        return Entity.query.all()

    @staticmethod
    def get_by_id(id: int) -> Entity:
        return Entity.query.get(id)

    @staticmethod
    def update(entity: Entity, Entity_change_updates: EntityInterface) -> Entity:
        entity.update(Entity_change_updates)
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
    def create(new_attrs: EntityInterface) -> Entity:
        new_entity = Entity(name=new_attrs["name"], purpose=new_attrs["purpose"])

        db.session.add(new_entity)
        db.session.commit()

        return new_entity