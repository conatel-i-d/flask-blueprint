from mypy_extensions import TypedDict


class EntityInterface(TypedDict, total=False):
    id: int
    name: str
    purpose: str