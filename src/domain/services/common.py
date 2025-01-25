from collections.abc import Iterable
from uuid import UUID
from typing import Protocol, TypeVar


__all__ = ("HasUnitUuid", "HasUnitUuidT", "HasId", "get_ids")


class HasUnitUuid(Protocol):
    unit_uuid: UUID


HasUnitUuidT = TypeVar("HasUnitUuidT", bound=HasUnitUuid)


class HasId(Protocol):
    id: UUID


def get_ids(*args: Iterable[HasId]) -> set[UUID]:
    result: set[UUID] = set()
    for collection in args:
        for item in collection:
            result.add(item.id)
    return result
