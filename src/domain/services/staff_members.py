from collections.abc import Iterable
from collections import defaultdict
from uuid import UUID
from typing import Protocol

from domain.enums import StaffMemberStatus, StaffMemberType
from domain.services.common import HasUnitUuidT
from domain.entities import UnitStaffCountByPosition


INTERNS = (
    UUID("09b059ae5fceac4211eb7bf91936e79c"),
    UUID("09b059ae5fceac4211eb7bf91936f16d"),
    UUID("09b059ae5fceac4211eb7bf91936fb9f"),
    UUID("09b059ae5fceac4211eb7bf919370418"),
    UUID("09b059ae5fceac4211eb7bf91937028f"),
)
COURIERS = (
    UUID("09b059ae5fceac4211eb7bf91936ff29"),
    UUID("09b059ae5fceac4211eb7bf91937050e"),
    UUID("09b059ae5fceac4211eb7bf9193705f1"),
)
GENERAL = (
    UUID("000d3abf84c3bb2e11ebfc11012115db"),
    UUID("09b059ae5fceac4211eb7bf91936fd47"),
    UUID("09b059ae5fceac4211eb7bf91936f57c"),
    UUID("09b059ae5fceac4211eb7bf91936f68d"),
    UUID("09b059ae5fceac4211eb7bf91937001f"),
    UUID("09b059ae5fceac4211eb7bf91936f827"),
    UUID("09b059ae5fceac4211eb7bf91936f926"),
)
CANDIDATES = (
    UUID("09b059ae5fceac4211eb7bf91936fe34"),
    UUID("09b059ae5fceac4211eb7bf91936f45a"),
)
MANAGERS = (UUID("09b059ae5fceac4211eb7bf91936faa5"),)
SKIPPED = (UUID("09b059ae5fceac4211eb7bf9193701a7"),)


class StaffMember(Protocol):
    unit_uuid: UUID
    status: StaffMemberStatus
    staff_type: StaffMemberType
    position_id: UUID | None
    position_name: str | None


def group_by_unit_uuid(
    items: Iterable[HasUnitUuidT],
) -> dict[UUID, list[HasUnitUuidT]]:
    unit_uuid_to_items = defaultdict(list)
    for item in items:
        unit_uuid_to_items[item.unit_uuid].append(item)
    return dict(unit_uuid_to_items)


def compute_staff_count_by_position(
    staff_members: Iterable[StaffMember],
) -> list[UnitStaffCountByPosition]:
    units_staff_count_by_position: list[UnitStaffCountByPosition] = []

    grouped_staff_members = group_by_unit_uuid(staff_members).items()
    for unit_uuid, unit_staff_members in grouped_staff_members:
        managers_count: int = 0
        kitchen_members_count: int = 0
        couriers_count: int = 0
        candidates_count: int = 0
        interns_count: int = 0

        for staff_member in unit_staff_members:
            if staff_member.position_id is None:
                continue
            elif staff_member.position_id in SKIPPED:
                continue
            elif staff_member.position_id in MANAGERS:
                managers_count += 1
            elif staff_member.position_id in GENERAL:
                kitchen_members_count += 1
            elif staff_member.position_id in COURIERS:
                couriers_count += 1
            elif staff_member.position_id in CANDIDATES:
                candidates_count += 1
            elif staff_member.position_id in INTERNS:
                interns_count += 1
            else:
                print(f"Unknown staff position: {staff_member}")

        unit_staff_count_by_position = UnitStaffCountByPosition(
            unit_uuid=unit_uuid,
            managers_count=managers_count,
            kitchen_members_count=kitchen_members_count,
            couriers_count=couriers_count,
            candidates_count=candidates_count,
            interns_count=interns_count,
        )
        units_staff_count_by_position.append(unit_staff_count_by_position)

    return units_staff_count_by_position
