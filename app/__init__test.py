from flask import json

from app.test.fixtures import app, client # noqa


def test_app_creates(app): # noqa
    assert app
    
def test_app_healthy(app, client): # noqa
    with client:
        resp = client.get('/healthz')
        data = json.loads(resp.data)
        assert resp.status_code == 200
        assert data['ok'] == True