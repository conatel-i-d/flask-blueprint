from sqlalchemy import Integer, Column, String
from app import db  # noqa
from .interface import EntityInterface


class Entity(db.Model):  # type: ignore
    """A snazzy Entity"""

    __tablename__ = "entity"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    purpose = Column(String(255))

    def update(self, changes: EntityInterface):
        for key, val in changes.items():
            setattr(self, key, val)
        return self