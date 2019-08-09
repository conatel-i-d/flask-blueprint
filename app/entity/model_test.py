from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from app.test.fixtures import app, db  # noqa
from .model import Entity


@fixture
def entity() -> Entity:
    return Entity(id=1, name="Test entity", purpose="Test purpose")


def test_Entity_create(entity: Entity):
    assert entity


def test_Entity_retrieve(entity: Entity, db: SQLAlchemy):  # noqa
    db.session.add(entity)
    db.session.commit()
    s = Entity.query.first()
    assert s.__dict__ == entity.__dict__