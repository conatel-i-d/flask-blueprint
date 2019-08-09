  
from .model import Entity  # noqa
from .schema import EntitySchema  # noqa

BASE_ROUTE = "entity"


def register_routes(api, app, root="api"):
    from .controller import api as entity_api

    api.add_namespace(entity_api, path=f"/{root}/{BASE_ROUTE}")