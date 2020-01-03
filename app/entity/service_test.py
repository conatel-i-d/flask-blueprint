from flask import g

from app.test.fixtures import app, db  # noqa
from .model import Entity
from .service import EntityService  # noqa


def test_get_all(db):  # noqa
    yin = Entity(id=1, name="Yin", purpose="thing 2")
    yang = Entity(id=2, name="Yang", purpose="thing 1")
    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()
    results = EntityService.get_all()
    assert len(results) == 2
    assert yin in results and yang in results

def test_get_all_ordered_by_purpose(db, app):  # noqa
    with app.app_context():
        g.order_by = 'purpose'
        yin = Entity(id=1, name="Yin", purpose="thing 2")
        yang = Entity(id=2, name="Yang", purpose="thing 1")
        db.session.add(yin)
        db.session.add(yang)
        db.session.commit()
        results = EntityService.get_all()
        assert len(results) == 2
        assert results[0] == yang

def test_get_all_ordered_by_purpose_desc(db, app):  # noqa
    with app.app_context():
        g.order_by = 'purpose'
        g.order_dir = 'desc'
        yin = Entity(id=1, name="Yin", purpose="thing 2")
        yang = Entity(id=2, name="Yang", purpose="thing 1")
        db.session.add(yin)
        db.session.add(yang)
        db.session.commit()
        results = EntityService.get_all()
        assert len(results) == 2
        assert results[0] == yin

def test_get_all_ordered_by_invalid_column_doesnt_fail(db, app):  # noqa
    with app.app_context():
        g.order_by = 'purpose'
        g.order_dir = 'desc'
        yin = Entity(id=1, name="Yin", purpose="thing 2")
        yang = Entity(id=2, name="Yang", purpose="thing 1")
        db.session.add(yin)
        db.session.add(yang)
        db.session.commit()
        results = EntityService.get_all()
        assert len(results) == 2

def test_update(db):  # noqa
    yin = Entity(id=1, name="Yin", purpose="thing 1")
    db.session.add(yin)
    db.session.commit()
    updates = dict(name="should not change", purpose="New purpose")
    EntityService.update(yin.id, updates)
    result = Entity.query.get(yin.id)
    assert result.name == "Yin"
    assert result.purpose == "New purpose"


def test_delete_by_id(db):  # noqa
    yin = Entity(id=1, name="Yin", purpose="thing 1")
    yang = Entity(id=2, name="Yang", purpose="thing 2")
    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()
    EntityService.delete_by_id(1)
    db.session.commit()
    results = Entity.query.all()
    assert len(results) == 1
    assert yin not in results and yang in results


def test_create(db):  # noqa
    yin = dict(name="Fancy new entity", purpose="Fancy new purpose")
    EntityService.create(yin)
    results = Entity.query.all()
    assert len(results) == 1
    for k in yin.keys():
        assert getattr(results[0], k) == yin[k]