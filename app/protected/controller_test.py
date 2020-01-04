from unittest.mock import patch
from flask.testing import FlaskClient
from flask import json, request
import pytest

from app.test.fixtures import client, app  # noqa
from app.api_response import ApiResponse
from .controller import ProtectedEntityResource
from .service import ProtectedEntityService
from .model import ProtectedEntity
from . import BASE_ROUTE

@pytest.fixture
def resource():
    return ProtectedEntityResource()

def make_entity(
    id: int = 123, name: str = "Test entity", purpose: str = "Test purpose", snake_case="Something"
) -> ProtectedEntity:
    return ProtectedEntity(id=id, name=name, purpose=purpose, snake_case=snake_case)


class TestProtectedEntityResource:
    @patch.object(
        ProtectedEntityService,
        "get_all",
        lambda: [
            make_entity(123, name="Test ProtectedEntity 1"),
            make_entity(456, name="Test ProtectedEntity 2"),
        ],
    )

    def test_get(self, client):
        """Should get the list of entities."""
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/").get_json()
            expected = dict(
                items=[
                    {'id': 123, 'name': 'Test ProtectedEntity 1', 'purpose': 'Test purpose', 'camelCase': 'Something'},
                    {'id': 456, 'name': 'Test ProtectedEntity 2', 'purpose': 'Test purpose', 'camelCase': 'Something'}
                ],
                count=2,
                current='http://localhost/api/entity/?page=1&per_page=3',
                next='http://localhost/api/entity/?page=2&per_page=3'
            )
            assert result == expected
    
    @patch.object(
        ProtectedEntityService, "create", lambda create_request: make_entity(**{**{'id': 1}, **create_request})
    )
    def test_post(self, client):  # noqa
        with client:
            data = dict(name='Test ProtectedEntity 1', purpose='Test purpose', camelCase='Something')
            result = client.post(f"/api/{BASE_ROUTE}/", json=data).get_json()
            expected = dict(item=dict(
                id=1,
                name='Test ProtectedEntity 1',
                camelCase='Something',
                purpose='Test purpose'))
            print(f"result = ", result)
            print(f"expected = ", expected)
            assert result == expected


def fake_update(id: int, changes) -> ProtectedEntity:
    # To fake an update, just return a new object
    updated_ProtectedEntity = ProtectedEntity(
        id=id, name=changes["name"], purpose=changes["purpose"]
    )
    return updated_ProtectedEntity


class TestProtectedEntityIdResource:
    @patch.object(ProtectedEntityService, "get_by_id", lambda id: make_entity(id=id))
    def test_get(self, client: FlaskClient):  # noqa
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/123").get_json()
            expected = dict(item=dict(id=123, name='Test entity', purpose='Test purpose', camelCase='Something'))
            print(f"result = ", result)
            print(f"expected = ", expected)
            assert result == expected

    @patch.object(ProtectedEntityService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):  # noqa
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/123")
            assert result.status_code == 204
            assert result.data == b''

    @patch.object(ProtectedEntityService, 'update', lambda id, update: dict(**{**update, **dict(id=123)}))
    def test_put(self, client: FlaskClient):  # noqa
        with client:
            updates = dict(name='New ProtectedEntity', purpose='New purpose')
            result = client.put(f"/api/{BASE_ROUTE}/123", json=updates).get_json()
            expected = dict(item=dict(**{**updates, **dict(id=123)}))
            assert result == expected
