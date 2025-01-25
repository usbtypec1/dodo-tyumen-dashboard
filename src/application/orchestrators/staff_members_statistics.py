from dataclasses import dataclass
from collections.abc import Iterable

from application.interactors.staff_positions_history_fetch import (
    StaffPositionsHistoryFetchInteractor,
)
from application.interactors.active_staff_members_fetch import (
    ActiveStaffMembersFetchInteractor,
)
from application.interactors.dismissed_staff_members_fetch import (
    DismissedStaffMembersFetchInteractor,
)
from domain.entities import Unit, UnitWeeklyStaffData
from domain.services.common import get_ids
from domain.services.staff_members import (
    merge_active_and_dismissed_staff_members_count,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffMembersStatisticsOrchestrator:
    units: Iterable[Unit]
    month: int
    year: int
    week: int
    active_staff_members_fetch_interactor: ActiveStaffMembersFetchInteractor
    dismissed_staff_members_fetch_interactor: DismissedStaffMembersFetchInteractor
    staff_positions_history_fetch_interactor: StaffPositionsHistoryFetchInteractor

    def execute(self) -> list[UnitWeeklyStaffData]:
        active_staff_members = self.active_staff_members_fetch_interactor.execute()
        dismissed_staff_members = (
            self.dismissed_staff_members_fetch_interactor.execute()
        )
        staff_member_ids = get_ids(
            active_staff_members,
            dismissed_staff_members,
        )
        staff_positions_history = self.staff_positions_history_fetch_interactor.execute(
            staff_member_ids
        )

        return merge_active_and_dismissed_staff_members_count(
            active_staff_members=active_staff_members,
            dismissed_staff_members=dismissed_staff_members,
            staff_positions_history=staff_positions_history,
            units=self.units,
            year=self.year,
            month=self.month,
            week=self.week,
        )
