from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

import pendulum

from domain.entities import UnitStaffCountByPosition
from domain.enums import StaffMemberStatus
from domain.services.staff_members import compute_staff_count_by_position
from infrastructure.dodo_is_api.models import StaffMember
from infrastructure.dodo_is_api.response_parsers import (
    parse_staff_members_response,
)
from domain.services.period import get_week_period
from application.interactors.dodo_is_api_fetch import DodoIsApiFetchInteractor


__all__ = ("ActiveStaffMembersFetchInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class ActiveStaffMembersFetchInteractor(DodoIsApiFetchInteractor):
    unit_uuids: Iterable[UUID]
    year: int
    month: int
    week: int
    timezone: pendulum.Timezone

    def execute(self) -> list[UnitStaffCountByPosition]:
        take: int = 1000
        skip: int = 0

        staff_members: list[StaffMember] = []

        period = get_week_period(
            year=self.year,
            month=self.month,
            week=self.week,
            timezone=self.timezone,
        )
        hired_to_date = period.from_date

        while True:
            response = self.dodo_is_api_connection.get_staff_members(
                unit_uuids=self.unit_uuids,
                take=take,
                skip=skip,
                statuses=(StaffMemberStatus.ACTIVE,),
                hired_to_date=hired_to_date,
            )
            staff_members_response = parse_staff_members_response(response)
            staff_members += staff_members_response.members

            if staff_members_response.is_end_of_list_reached:
                break

            skip += take

        return compute_staff_count_by_position(staff_members)
