from app.utils.base_service import BaseService
from .model import Entity
from .interfaces import EntityInterfaces


class EntityService(BaseService):
    model = Entity
    interfaces = EntityInterfaces
