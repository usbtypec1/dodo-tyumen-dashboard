import argparse

from fast_depends import inject

from infrastructure.dependencies.config import ConfigDependency
from infrastructure.dependencies.storage import StorageGatewayDependency
from application.interactors.monthly_sales_fetch import (
    MonthlySalesFetchInteractor,
)
from infrastructure.dependencies.dodo_is_api import (
    DodoIsApiConnectionDependency,
)
from domain.services.period import Period
from domain.services.units import to_uuids
from application.orchestrators.economics_statistics import (
    EconomicsStatisticsOrchestrator,
)
from application.interactors.delivery_statistics_fetch import (
    DeliveryStatisticsForMonthFetchInteractor,
)
from application.interactors.productivity_statistics_fetch import (
    ProductivityStatisticsForMonthFetchInteractor,
)
from application.interactors.unit_monthly_goals_fetch import (
    UnitMonthlyGoalsFetchInteractor,
)


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

    if year is None:
        year = period.from_date.year
    if month is None:
        month = period.from_date.month

    unit_uuids = to_uuids(config.units)
    delivery_statistics_fetch_interactor = DeliveryStatisticsForMonthFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        month=month,
        year=year,
        timezone=config.timezone,
        unit_uuids=unit_uuids,
    )
    producitivty_statistics_fetch_interactor = (
        ProductivityStatisticsForMonthFetchInteractor(
            dodo_is_api_connection=dodo_is_api_connection,
            month=month,
            year=year,
            timezone=config.timezone,
            unit_uuids=unit_uuids,
        )
    )
    unit_monthly_goals_fetch_interactors = [
        UnitMonthlyGoalsFetchInteractor(
            dodo_is_api_connection=dodo_is_api_connection,
            month=month,
            year=year,
            unit_uuid=unit_uuid,
        )
        for unit_uuid in unit_uuids
    ]
    monthly_sales_fetch_interactor = MonthlySalesFetchInteractor(
        dodo_is_api_connection=dodo_is_api_connection,
        month=month,
        year=year,
        timezone=config.timezone,
        unit_uuids=unit_uuids,
    )

    economics_statistics_orchestrator = EconomicsStatisticsOrchestrator(
        units=config.units,
        year=year,
        month=month,
        delivery_statistics_fetch_interactor=delivery_statistics_fetch_interactor,
        produciton_statistics_fetch_interactor=producitivty_statistics_fetch_interactor,
        unit_monthly_goals_fetch_intetactors=unit_monthly_goals_fetch_interactors,
        monthly_sales_fetch_interactor=monthly_sales_fetch_interactor,
    )
    units_monthly_economics_data = economics_statistics_orchestrator.execute()

    storage_gateway.add_units_economics_data(units_monthly_economics_data)


if __name__ == "__main__":
    main()  # type: ignore[reportCallIssue]
