  
from .model import ProtectedEntity  # noqa

BASE_ROUTE = "protected-entity"


def register_routes(api, app, root="api"):
    from .controller import api as protected_entity_api

    api.add_namespace(protected_entity_api, path=f"/{root}/{BASE_ROUTE}")