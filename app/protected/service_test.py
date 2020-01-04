from flask import g

from app.test.fixtures import app, db  # noqa
from .model import ProtectedEntity
from .service import ProtectedEntityService  # noqa


def test_get_all(db):  # noqa
    yin = ProtectedEntity(id=1, name="Yin", purpose="thing 2")
    yang = ProtectedEntity(id=2, name="Yang", purpose="thing 1")
    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()
    results = ProtectedEntityService.get_all()
    assert len(results) == 2
    assert yin in results and yang in results

def test_get_all_ordered_by_purpose(db, app):  # noqa
    with app.app_context():
        g.order_by = 'purpose'
        yin = ProtectedEntity(id=1, name="Yin", purpose="thing 2")
        yang = ProtectedEntity(id=2, name="Yang", purpose="thing 1")
        db.session.add(yin)
        db.session.add(yang)
        db.session.commit()
        results = ProtectedEntityService.get_all()
        assert len(results) == 2
        assert results[0] == yang

def test_get_all_ordered_by_purpose_desc(db, app):  # noqa
    with app.app_context():
        g.order_by = 'purpose'
        g.order_dir = 'desc'
        yin = ProtectedEntity(id=1, name="Yin", purpose="thing 2")
        yang = ProtectedEntity(id=2, name="Yang", purpose="thing 1")
        db.session.add(yin)
        db.session.add(yang)
        db.session.commit()
        results = ProtectedEntityService.get_all()
        assert len(results) == 2
        assert results[0] == yin

def test_get_all_ordered_by_invalid_column_doesnt_fail(db, app):  # noqa
    with app.app_context():
        g.order_by = 'purpose'
        g.order_dir = 'desc'
        yin = ProtectedEntity(id=1, name="Yin", purpose="thing 2")
        yang = ProtectedEntity(id=2, name="Yang", purpose="thing 1")
        db.session.add(yin)
        db.session.add(yang)
        db.session.commit()
        results = ProtectedEntityService.get_all()
        assert len(results) == 2

def test_update(db):  # noqa
    yin = ProtectedEntity(id=1, name="Yin", purpose="thing 1")
    db.session.add(yin)
    db.session.commit()
    updates = dict(name="should not change", purpose="New purpose")
    ProtectedEntityService.update(yin.id, updates)
    result = ProtectedEntity.query.get(yin.id)
    assert result.name == "Yin"
    assert result.purpose == "New purpose"


def test_delete_by_id(db):  # noqa
    yin = ProtectedEntity(id=1, name="Yin", purpose="thing 1")
    yang = ProtectedEntity(id=2, name="Yang", purpose="thing 2")
    db.session.add(yin)
    db.session.add(yang)
    db.session.commit()
    ProtectedEntityService.delete_by_id(1)
    db.session.commit()
    results = ProtectedEntity.query.all()
    assert len(results) == 1
    assert yin not in results and yang in results


def test_create(db):  # noqa
    yin = dict(name="Fancy new entity", purpose="Fancy new purpose")
    ProtectedEntityService.create(yin)
    results = ProtectedEntity.query.all()
    assert len(results) == 1
    for k in yin.keys():
        assert getattr(results[0], k) == yin[k]