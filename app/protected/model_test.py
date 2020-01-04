from pytest import fixture
from flask_sqlalchemy import SQLAlchemy
from app.test.fixtures import app, db  # noqa
from .model import ProtectedEntity


@fixture
def entity() -> ProtectedEntity:
    return ProtectedEntity(id=1, name="Test entity", purpose="Test purpose")


def test_ProtectedEntity_create(entity: ProtectedEntity):
    assert entity


def test_ProtectedEntity_retrieve(entity: ProtectedEntity, db: SQLAlchemy):  # noqa
    db.session.add(entity)
    db.session.commit()
    s = ProtectedEntity.query.first()
    assert s.__dict__ == entity.__dict__