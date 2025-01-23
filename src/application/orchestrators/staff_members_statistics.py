from dataclasses import dataclass
from collections.abc import Iterable

from application.interactors.active_staff_members_fetch import (
    ActiveStaffMembersFetchInteractor,
)
from application.interactors.dismissed_staff_members_fetch import (
    DismissedStaffMembersFetchInteractor,
)
from domain.entities import Unit, UnitWeeklyStaffData
from domain.services.units import map_unit_uuid_to_item


@dataclass(frozen=True, slots=True, kw_only=True)
class StaffMembersStatisticsOrchestrator:
    units: Iterable[Unit]
    month: int
    year: int
    week: int
    active_staff_members_fetch_interactor: ActiveStaffMembersFetchInteractor
    dismissed_staff_members_fetch_interactor: (
        DismissedStaffMembersFetchInteractor
    )

    def execute(self) -> list[UnitWeeklyStaffData]:
        active_staff_members_count_by_position = (
            self.active_staff_members_fetch_interactor.execute()
        )
        dismissed_staff_members_count_by_position = (
            self.dismissed_staff_members_fetch_interactor.execute()
        )

        unit_uuid_to_active_staff_memebrs = map_unit_uuid_to_item(
            active_staff_members_count_by_position
        )
        unit_uuid_to_dismissed_staff_members = map_unit_uuid_to_item(
            dismissed_staff_members_count_by_position
        )
        
        units_weekly_staff_data: list[UnitWeeklyStaffData] = []

        for unit in self.units:
            active_staff_members = unit_uuid_to_active_staff_memebrs.get(
                unit.uuid
            )
            dismissed_staff_members = unit_uuid_to_dismissed_staff_members.get(
                unit.uuid
            )

            active_managers_count: int = 0
            active_kitchen_members_count: int = 0
            active_couriers_count: int = 0
            active_candidates_count: int = 0
            active_interns_count: int = 0
            if active_staff_members is not None:
                active_managers_count = active_staff_members.managers_count
                active_kitchen_members_count = (
                    active_staff_members.kitchen_members_count
                )
                active_couriers_count = active_staff_members.couriers_count
                active_candidates_count = active_staff_members.candidates_count
                active_interns_count = active_staff_members.interns_count

            dismissed_managers_count: int = 0
            dismissed_kitchen_members_count: int = 0
            dismissed_couriers_count: int = 0
            dismissed_candidates_count: int = 0
            dismissed_interns_count: int = 0

            if dismissed_staff_members is not None:
                dismissed_managers_count = (
                    dismissed_staff_members.managers_count
                )
                dismissed_kitchen_members_count = (
                    dismissed_staff_members.kitchen_members_count
                )
                dismissed_couriers_count = (
                    dismissed_staff_members.couriers_count
                )
                dismissed_candidates_count = (
                    dismissed_staff_members.candidates_count
                )
                dismissed_interns_count = dismissed_staff_members.interns_count

            unit_weekly_staff_data = UnitWeeklyStaffData(
                unit_name=unit.name,
                year=self.year,
                month=self.month,
                week=self.week,
                active_managers_count=active_managers_count,
                active_kitchen_members_count=active_kitchen_members_count,
                active_couriers_count=active_couriers_count,
                active_candidates_count=active_candidates_count,
                active_interns_count=active_interns_count,
                dismissed_managers_count=dismissed_managers_count,
                dismissed_kitchen_members_count=dismissed_kitchen_members_count,
                dismissed_couriers_count=dismissed_couriers_count,
                dismissed_candidates_count=dismissed_candidates_count,
                dismissed_interns_count=dismissed_interns_count,
                new_candidates_count=0,
                new_specialists_count=0,
            )
            units_weekly_staff_data.append(unit_weekly_staff_data)
        
        return units_weekly_staff_data
