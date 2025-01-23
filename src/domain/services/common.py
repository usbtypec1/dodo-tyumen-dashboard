from uuid import UUID
from typing import Protocol, TypeVar


__all__ = ("HasUnitUuid", "HasUnitUuidT")


class HasUnitUuid(Protocol):
    unit_uuid: UUID


HasUnitUuidT = TypeVar("HasUnitUuidT", bound=HasUnitUuid)
