from collections.abc import Iterable
import sqlite3
from uuid import UUID

import gspread
import pendulum

from domain.entities import Unit
from infrastructure.storage import StorageGateway
from application.interactors.monthly_sales_fetch import (
    MonthlySalesFetchInteractor,
)
from domain.services.period import Period
from bootstrap.config import (
    GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH,
    load_config_from_file,
)
from domain.services.units import to_uuids
from infrastructure.auth_credentials import AuthCredentialsGateway
from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from infrastructure.dodo_is_api.http_client import (
    closing_dodo_is_api_http_client,
)
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


def process(
    *,
    connection: DodoIsApiConnection,
    month: int,
    year: int,
    timezone: pendulum.Timezone,
    units: Iterable[Unit],
):
    unit_uuids = to_uuids(units)
    delivery_statistics_fetch_interactor = (
        DeliveryStatisticsForMonthFetchInteractor(
            dodo_is_api_connection=connection,
            month=month,
            year=year,
            timezone=timezone,
            unit_uuids=unit_uuids,
        )
    )
    producitivty_statistics_fetch_interactor = (
        ProductivityStatisticsForMonthFetchInteractor(
            dodo_is_api_connection=connection,
            month=month,
            year=year,
            timezone=timezone,
            unit_uuids=unit_uuids,
        )
    )
    unit_monthly_goals_fetch_interactors = [
        UnitMonthlyGoalsFetchInteractor(
            dodo_is_api_connection=connection,
            month=month,
            year=year,
            unit_uuid=unit_uuid,
        )
        for unit_uuid in unit_uuids
    ]
    monthly_sales_fetch_interactor = MonthlySalesFetchInteractor(
        dodo_is_api_connection=connection,
        month=month,
        year=year,
        timezone=timezone,
        unit_uuids=unit_uuids,
    )

    economics_statistics_orchestrator = EconomicsStatisticsOrchestrator(
        units=units,
        year=year,
        month=month,
        delivery_statistics_fetch_interactor=delivery_statistics_fetch_interactor,
        produciton_statistics_fetch_interactor=producitivty_statistics_fetch_interactor,
        unit_monthly_goals_fetch_intetactors=unit_monthly_goals_fetch_interactors,
        monthly_sales_fetch_interactor=monthly_sales_fetch_interactor,
    )
    units_monthly_economics_data = economics_statistics_orchestrator.execute()

    with sqlite3.connect("./database.db") as db_connection:
        storage_gateway = StorageGateway(connection=db_connection)
        storage_gateway.add_units_economics_data(units_monthly_economics_data)


def main():
    config = load_config_from_file()

    service_account = gspread.service_account(  # type: ignore[reportPrivateImportUsage]
        GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH
    )
    auth_credentials_gateway = AuthCredentialsGateway(
        service_account=service_account,
        spreadsheet_id=config.auth_credentials.spreadsheet_id,
        credentials_sheet_id=config.auth_credentials.sheet_id,
    )
    access_token = auth_credentials_gateway.get_access_token()

    period = Period.current_month(config.timezone)

    # year = period.from_date.year
    # month = period.from_date.month

    with closing_dodo_is_api_http_client(
        base_url=config.dodo_is_api.base_url,
        access_token=access_token,
    ) as http_client:
        connection = DodoIsApiConnection(http_client=http_client)
        year = 2024
        for month in range(1, 12):
            process(
                connection=connection,
                month=month,
                year=year,
                timezone=config.timezone,
                units=config.units,
            )


if __name__ == "__main__":
    main()
