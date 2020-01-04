from app.utils.base_service import BaseService
from .model import ProtectedEntity
from .interfaces import ProtectedEntityInterfaces


class ProtectedEntityService(BaseService):
    model = ProtectedEntity
    interfaces = ProtectedEntityInterfaces
