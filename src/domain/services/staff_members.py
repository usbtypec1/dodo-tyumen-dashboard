from collections.abc import Iterable
from collections import defaultdict
from dataclasses import dataclass
from uuid import UUID
from typing import Protocol

from domain.enums import StaffMemberStatus, StaffMemberType
from domain.services.common import HasUnitUuidT
from domain.entities import UnitStaffCountByPosition, Unit, UnitWeeklyStaffData
from domain.services.units import map_unit_uuid_to_item


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
SPECIALIST = (
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
    id: UUID
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
    specialist_staff_member_ids: Iterable[UUID],
) -> list[UnitStaffCountByPosition]:
    units_staff_count_by_position: list[UnitStaffCountByPosition] = []
    specialist_staff_member_ids = set(specialist_staff_member_ids)

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
            elif staff_member.position_id in SPECIALIST:
                kitchen_members_count += 1
            elif staff_member.position_id in COURIERS:
                couriers_count += 1
            elif staff_member.position_id in CANDIDATES:
                if staff_member.id in specialist_staff_member_ids:
                    kitchen_members_count += 1
                else:
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


class HasStaffIdAndPositionId(Protocol):
    staff_id: UUID
    position_id: UUID


def get_specialist_staff_member_ids(
    staff_positions_history: Iterable[HasStaffIdAndPositionId],
) -> set[UUID]:
    """
    Get the IDs of staff members who were specialists.

    Args:
        An iterable of staff position history records.

    Returns:
        A set of UUIDs of staff members who were specialists.
    """
    return {
        staff_position.staff_id
        for staff_position in staff_positions_history
        if staff_position.position_id in SPECIALIST
    }


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffCountByPosition:
    managers_count: int = 0
    kitchen_members_count: int = 0
    couriers_count: int = 0
    candidates_count: int = 0
    interns_count: int = 0


def get_staff_members_count_by_position(
    unit_staff_members_count_by_position: UnitStaffCountByPosition | None,
) -> StaffCountByPosition:
    if unit_staff_members_count_by_position is None:
        return StaffCountByPosition()
    return StaffCountByPosition(
        managers_count=unit_staff_members_count_by_position.managers_count,
        kitchen_members_count=unit_staff_members_count_by_position.kitchen_members_count,
        couriers_count=unit_staff_members_count_by_position.couriers_count,
        candidates_count=unit_staff_members_count_by_position.candidates_count,
        interns_count=unit_staff_members_count_by_position.interns_count,
    )


def merge_unit_active_and_dismissed_staff_members_count(
    *,
    unit_name: str,
    year: int,
    month: int,
    week: int,
    unit_active_staff_members: UnitStaffCountByPosition | None,
    unit_dismissed_staff_members: UnitStaffCountByPosition | None,
) -> UnitWeeklyStaffData:
    active_staff_count_by_position = get_staff_members_count_by_position(
        unit_active_staff_members
    )
    dismissed_staff_count_by_position = get_staff_members_count_by_position(
        unit_dismissed_staff_members
    )
    return UnitWeeklyStaffData(
        unit_name=unit_name,
        year=year,
        month=month,
        week=week,
        active_managers_count=active_staff_count_by_position.managers_count,
        active_kitchen_members_count=active_staff_count_by_position.kitchen_members_count,
        active_couriers_count=active_staff_count_by_position.couriers_count,
        active_candidates_count=active_staff_count_by_position.candidates_count,
        active_interns_count=active_staff_count_by_position.interns_count,
        dismissed_managers_count=dismissed_staff_count_by_position.managers_count,
        dismissed_kitchen_members_count=dismissed_staff_count_by_position.kitchen_members_count,
        dismissed_couriers_count=dismissed_staff_count_by_position.couriers_count,
        dismissed_candidates_count=dismissed_staff_count_by_position.candidates_count,
        dismissed_interns_count=dismissed_staff_count_by_position.interns_count,
        new_candidates_count=0,
        new_specialists_count=0,
    )


def merge_active_and_dismissed_staff_members_count(
    *,
    active_staff_members: Iterable[StaffMember],
    dismissed_staff_members: Iterable[StaffMember],
    staff_positions_history: Iterable[HasStaffIdAndPositionId],
    units: Iterable[Unit],
    year: int,
    month: int,
    week: int,
):
    specialist_staff_member_ids = get_specialist_staff_member_ids(
        staff_positions_history=staff_positions_history,
    )

    active_staff_members_count_by_position = compute_staff_count_by_position(
        staff_members=active_staff_members,
        specialist_staff_member_ids=specialist_staff_member_ids,
    )
    dismissed_staff_members_count_by_position = compute_staff_count_by_position(
        staff_members=dismissed_staff_members,
        specialist_staff_member_ids=specialist_staff_member_ids,
    )
    unit_uuid_to_active_staff_memebrs = map_unit_uuid_to_item(
        active_staff_members_count_by_position
    )
    unit_uuid_to_dismissed_staff_members = map_unit_uuid_to_item(
        dismissed_staff_members_count_by_position
    )

    units_weekly_staff_data: list[UnitWeeklyStaffData] = []

    for unit in units:
        unit_active_staff_members_count_by_position = (
            unit_uuid_to_active_staff_memebrs.get(unit.uuid)
        )
        unit_dismissed_staff_members_count_by_position = (
            unit_uuid_to_dismissed_staff_members.get(unit.uuid)
        )
        units_weekly_staff_data.append(
            merge_unit_active_and_dismissed_staff_members_count(
                unit_name=unit.name,
                year=year,
                month=month,
                week=week,
                unit_active_staff_members=unit_active_staff_members_count_by_position,
                unit_dismissed_staff_members=unit_dismissed_staff_members_count_by_position,
            )
        )

    return units_weekly_staff_data
