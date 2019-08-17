from flask_sqlalchemy import SQLAlchemy
from typing import List
from app.test.fixtures import app, db  # noqa
from .model import Entity
from .service import EntityService  # noqa


def test_get_all(db: SQLAlchemy):  # noqa
    yin: Entity = Entity(id=1, name="Yin", purpose="thing 1")
    yang: Entity = Entity(id=2, name="Yang", purpose="thing 2")
    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()

    results: List[Entity] = EntityService.get_all()

    assert len(results) == 2
    assert yin in results and yang in results


def test_update(db: SQLAlchemy):  # noqa
    yin: Entity = Entity(id=1, name="Yin", purpose="thing 1")

    db.session.add(yin)
    db.session.commit()
    updates: EntityInterface = dict(name="New Entity name")

    EntityService.update(yin, updates)

    result: Entity = Entity.query.get(yin.id)
    assert result.name == "New Entity name"


def test_delete_by_id(db: SQLAlchemy):  # noqa
    yin: Entity = Entity(id=1, name="Yin", purpose="thing 1")
    yang: Entity = Entity(id=2, name="Yang", purpose="thing 2")
    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()

    EntityService.delete_by_id(1)
    db.session.commit()

    results: List[Entity] = Entity.query.all()

    assert len(results) == 1
    assert yin not in results and yang in results


def test_create(db: SQLAlchemy):  # noqa

    yin: EntityInterface = dict(name="Fancy new entity", purpose="Fancy new purpose")
    EntityService.create(yin)
    results: List[Entity] = Entity.query.all()

    assert len(results) == 1

    for k in yin.keys():
        assert getattr(results[0], k) == yin[k]