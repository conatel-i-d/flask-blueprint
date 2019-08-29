from unittest.mock import patch
from flask.testing import FlaskClient
from flask import json, request
import pytest

from app.test.fixtures import client, app  # noqa
from app.api_response import ApiResponse
from .controller import EntityResource
from .service import EntityService
from .schema import EntitySchema
from .model import Entity
from . import BASE_ROUTE

@pytest.fixture
def resource():
    return EntityResource()

def make_entity(
    id: int = 123, name: str = "Test entity", purpose: str = "Test purpose", snake_case="Something"
) -> Entity:
    return Entity(id=id, name=name, purpose=purpose, snake_case=snake_case)


class TestEntityResource:
    @patch.object(
        EntityService,
        "get_all",
        lambda: [
            make_entity(123, name="Test Entity 1"),
            make_entity(456, name="Test Entity 2"),
        ],
    )

    def test_get(self, client):
        """Should get the list of entities."""
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/").get_json()
            expected = dict(
                items=[
                    {'id': 123, 'name': 'Test Entity 1', 'purpose': 'Test purpose'},
                    {'id': 456, 'name': 'Test Entity 2', 'purpose': 'Test purpose'}
                ],
                count=2
            )
            print(f"result = ", result)
            print(f"expected = ", expected)
            assert result == expected
    
    @patch.object(
        EntityService, "create", lambda create_request: make_entity(**{**{'id': 1}, **create_request})
    )
    def test_post(self, client):  # noqa
        with client:
            data = dict(name='Test Entity 1', purpose='Test purpose', camelCase='Something')
            result = client.post(f"/api/{BASE_ROUTE}/", json=data).get_json()
            expected = dict(item=dict(
                id=1,
                name='Test Entity 1',
                snake_case='Something',
                purpose='Test purpose'))
            print(f"result = ", result)
            print(f"expected = ", expected)
            assert result == expected


def fake_update(id: int, changes) -> Entity:
    # To fake an update, just return a new object
    updated_Entity = Entity(
        id=id, name=changes["name"], purpose=changes["purpose"]
    )
    return updated_Entity


class TestEntityIdResource:
    @patch.object(EntityService, "get_by_id", lambda id: make_entity(id=id))
    def test_get(self, client: FlaskClient):  # noqa
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/123").get_json()
            expected = dict(item=dict(id=123, name='Test entity', purpose='Test purpose'))
            print(f"result = ", result)
            print(f"expected = ", expected)
            assert result == expected

    @patch.object(EntityService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):  # noqa
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/123")
            assert result.status_code == 204
            assert result.data == b''

    @patch.object(EntityService, 'update', lambda id, update: dict(**{**update, **dict(id=123)}))
    def test_put(self, client: FlaskClient):  # noqa
        with client:
            updates = dict(name='New Entity', purpose='New purpose')
            result = client.put(f"/api/{BASE_ROUTE}/123", json=updates).get_json()
            expected = dict(item=dict(**{**updates, **dict(id=123)}))
            assert result == expected