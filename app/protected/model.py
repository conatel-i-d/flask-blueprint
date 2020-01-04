from sqlalchemy import Integer, Column, String
from app import db  # noqa


class ProtectedEntity(db.Model):  # type: ignore
    """ProtectedEntity Model"""

    __tablename__ = "protected-entity"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    purpose = Column(String(255))
    snake_case = Column(String(255))

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self