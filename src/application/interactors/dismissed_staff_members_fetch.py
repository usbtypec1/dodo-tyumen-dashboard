from dataclasses import dataclass
from collections.abc import Iterable
from uuid import UUID

import pendulum

from domain.enums import StaffMemberStatus
from domain.entities import UnitStaffCountByPosition
from domain.services.period import get_week_period
from domain.services.staff_members import compute_staff_count_by_position
from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from infrastructure.dodo_is_api.models import StaffMember
from infrastructure.dodo_is_api.response_parsers import (
    parse_staff_members_response,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DismissedStaffMembersFetchInteractor:
    dodo_is_api_connection: DodoIsApiConnection
    year: int
    month: int
    week: int
    timezone: pendulum.Timezone
    unit_uuids: Iterable[UUID]

    def execute(self) -> list[UnitStaffCountByPosition]:
        take: int = 1000
        skip: int = 0

        period = get_week_period(
            year=self.year, month=self.month, week=self.week, timezone=self.timezone
        )

        staff_members: list[StaffMember] = []

        while True:
            response = self.dodo_is_api_connection.get_staff_members(
                unit_uuids=self.unit_uuids,
                take=take,
                skip=skip,
                dismissed_from_date=period.from_date,
                dismissed_to_date=period.to_date,
                statuses=(StaffMemberStatus.DISMISSED,),
            )
            staff_members_response = parse_staff_members_response(response)
            staff_members += staff_members_response.members

            if staff_members_response.is_end_of_list_reached:
                break

            skip += take

        return compute_staff_count_by_position(staff_members)
