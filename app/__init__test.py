from flask import json, g

from app.test.fixtures import app, client # noqa


def test_app_creates(app): # noqa
    assert app

def test_global_state(app, client): #noqa
    with client:
        response = client.get('/healthz')
        assert g.page == app.config['PAGE']
        assert g.per_page == app.config['PER_PAGE']

def test_app_healthy(app, client): # noqa
    with client:
        response = client.get('/healthz')
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['ok'] == True
