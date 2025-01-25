import argparse

from fast_depends import inject

from application.interactors.staff_positions_history_fetch import (
    StaffPositionsHistoryFetchInteractor,
)
from infrastructure.dependencies.config import ConfigDependency
from infrastructure.dependencies.dodo_is_api import (
    DodoIsApiConnectionDependency,
)
from infrastructure.dependencies.storage import StorageGatewayDependency
from domain.services.period import Period, get_current_week_number
from application.interactors.active_staff_members_fetch import (
    ActiveStaffMembersFetchInteractor,
)
from application.interactors.dismissed_staff_members_fetch import (
    DismissedStaffMembersFetchInteractor,
)
from application.orchestrators.staff_members_statistics import (
    StaffMembersStatisticsOrchestrator,
)
from domain.services.units import to_uuids


@inject
def main(
    config: ConfigDependency,
    dodo_is_api_connection: DodoIsApiConnectionDependency,
    storage_gateway: StorageGatewayDependency,
):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--year",
        type=int,
        required=False,
    )
    argument_parser.add_argument(
        "--month",
        type=int,
        required=False,
    )
    argument_parser.add_argument(
        "--week",
        type=int,
        required=False,
    )
    args = argument_parser.parse_args()

    period = Period.current_month(config.timezone)

    year: int | None = args.year
    month: int | None = args.month
    week: int | None = args.week

    if year is None:
        year = period.from_date.year
    if month is None:
        month = period.from_date.month
    if week is None:
        week = get_current_week_number(config.timezone)

    unit_uuids = to_uuids(config.units)
    active_staff_members_fetch_interactor = ActiveStaffMembersFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        unit_uuids=unit_uuids,
        year=year,
        month=month,
        week=week,
        timezone=config.timezone,
    )
    dismissed_staff_members_fetch_interactor = DismissedStaffMembersFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        year=year,
        month=month,
        week=week,
        timezone=config.timezone,
        unit_uuids=unit_uuids,
    )
    staff_positions_history_fetch_interactor = StaffPositionsHistoryFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
    )
    staff_members_statistics_orchestrator = StaffMembersStatisticsOrchestrator(
        units=config.units,
        year=year,
        month=month,
        week=week,
        active_staff_members_fetch_interactor=active_staff_members_fetch_interactor,
        dismissed_staff_members_fetch_interactor=dismissed_staff_members_fetch_interactor,
        staff_positions_history_fetch_interactor=staff_positions_history_fetch_interactor,
    )
    units_weekly_staff_data = staff_members_statistics_orchestrator.execute()

    storage_gateway.add_units_staff_data(units_weekly_staff_data)


if __name__ == "__main__":
    main()  # type: ignore[reportCallIssue]
