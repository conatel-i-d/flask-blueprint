from unittest.mock import patch
from flask.testing import FlaskClient
import pytest

from app.test.fixtures import client, app  # noqa
from app.api_response import ApiResponse
from .controller import EntityResource
from .service import EntityService
from .schema import EntitySchema
from .model import Entity
from .interface import EntityInterface
from . import BASE_ROUTE

@pytest.fixture
def resource():
    return EntityResource()

def make_entity(
    id: int = 123, name: str = "Test entity", purpose: str = "Test purpose"
) -> Entity:
    return Entity(id=id, name=name, purpose=purpose)


class TestEntityResource:
    @patch.object(
        EntityService,
        "get_all",
        lambda: [
            make_entity(123, name="Test Entity 1"),
            make_entity(456, name="Test Entity 2"),
        ],
    )
    def test_get(self, resource: EntityResource):  # noqa
        response = resource.get()
        expected = (
            EntitySchema(many=True)
            .dump(
                [
                    make_entity(123, name="Test Entity 1"),
                    make_entity(456, name="Test Entity 2"),
                ]
            )
            .data
        )
        assert isinstance(response, ApiResponse) == True
        assert response.status == 200
        for r in response.value:
            assert r in expected

    @patch.object(
        EntityService, "create", lambda create_request: Entity(**create_request)
    )
    def test_post(self, client: FlaskClient):  # noqa
        with client:

            payload = dict(name="Test entity", purpose="Test purpose")
            result = client.post(f"/api/{BASE_ROUTE}/", json=payload).get_json()
            expected = (
                EntitySchema()
                .dump(Entity(name=payload["name"], purpose=payload["purpose"]))
                .data
            )
            assert result == expected


def fake_update(entity: Entity, changes: EntityInterface) -> Entity:
    # To fake an update, just return a new object
    updated_Entity = Entity(
        id=entity.id, name=changes["name"], purpose=changes["purpose"]
    )
    return updated_Entity


class TestEntityIdResource:
    @patch.object(EntityService, "get_by_id", lambda id: make_entity(id=id))
    def test_get(self, client: FlaskClient):  # noqa
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/123").get_json()
            expected = make_entity(id=123)
            print(f"result = ", result)
            assert result["id"] == expected.id

    @patch.object(EntityService, "delete_by_id", lambda id: id)
    def test_delete(self, client: FlaskClient):  # noqa
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/123").get_json()
            expected = dict(status="Success", id=123)
            assert result == expected

    @patch.object(EntityService, "get_by_id", lambda id: make_entity(id=id))
    @patch.object(EntityService, "update", fake_update)
    def test_put(self, client: FlaskClient):  # noqa
        with client:
            result = client.put(
                f"/api/{BASE_ROUTE}/123",
                json={"name": "New Entity", "purpose": "New purpose"},
            ).get_json()
            expected = (
                EntitySchema()
                .dump(Entity(id=123, name="New Entity", purpose="New purpose"))
                .data
            )
            assert result == expected