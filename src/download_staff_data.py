import argparse

from fast_depends import inject

from application.interactors.staff_positions_history_fetch import (
    StaffPositionsHistoryFetchInteractor,
)
from bootstrap.config import Config
from infrastructure.dependencies.config import ConfigDependency
from infrastructure.dependencies.dodo_is_api import (
    DodoIsApiConnectionDependency,
)
from infrastructure.dependencies.storage import StorageGatewayDependency
from domain.services.period import (
    Period,
    get_current_week_number_of_year,
    get_month_number_by_week_number_of_year,
)
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
from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from infrastructure.storage import StorageGateway


def process(
    config: Config,
    year: int | None,
    week: int | None,
    dodo_is_api_connection: DodoIsApiConnection,
    storage_gateway: StorageGateway,
) -> None:
    period = Period.current_month(config.timezone)

    if year is None:
        year = period.from_date.year
    if week is None:
        week = get_current_week_number_of_year(config.timezone)

    month = get_month_number_by_week_number_of_year(week, year)

    unit_uuids = to_uuids(config.units)
    active_staff_members_fetch_interactor = ActiveStaffMembersFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        unit_uuids=unit_uuids,
        year=year,
        week=week,
        timezone=config.timezone,
    )
    dismissed_staff_members_fetch_interactor = DismissedStaffMembersFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        year=year,
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
        "--week",
        type=int,
        required=False,
    )
    args = argument_parser.parse_args()
    year: int | None = args.year
    week: int | None = args.week

    for year in range(2020, 2025):
        for week in range(1, 53):
            process(config, year, week, dodo_is_api_connection, storage_gateway)

    for year in range(2025, 2026):
        for week in range(1, 6):
            process(config, year, week, dodo_is_api_connection, storage_gateway)


if __name__ == "__main__":
    main()  # type: ignore[reportCallIssue]
