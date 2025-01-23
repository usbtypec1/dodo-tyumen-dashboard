from collections.abc import Iterable
from uuid import UUID
from typing import Protocol

from domain.services.common import HasUnitUuid, HasUnitUuidT


__all__ = ("get_unit_uuids", "map_unit_uuid_to_item", "to_uuids")


class HasUuid(Protocol):
    uuid: UUID


def get_unit_uuids(*collections_of_items: Iterable[HasUnitUuid]) -> set[UUID]:
    unit_uuids: set[UUID] = set()
    for items in collections_of_items:
        for item in items:
            unit_uuids.add(item.unit_uuid)
    return unit_uuids


def map_unit_uuid_to_item(
    items: Iterable[HasUnitUuidT],
) -> dict[UUID, HasUnitUuidT]:
    return {item.unit_uuid: item for item in items}


def to_uuids(items: Iterable[HasUuid]) -> set[UUID]:
    return {item.uuid for item in items}
