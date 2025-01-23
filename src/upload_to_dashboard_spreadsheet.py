import sqlite3

import gspread

from infrastructure.storage import StorageGateway
from infrastructure.dashboard import DashboardSpreadsheetGateway
from bootstrap.config import (
    GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH,
    load_config_from_file,
)


def main():
    config = load_config_from_file()
    service_account = gspread.service_account(  # type: ignore[reportPrivateImportUsage]
        GOOGLE_SHEETS_SERVICE_ACCOUNT_CREDENTIALS_FILE_PATH
    )

    dashboard_spreadsheet_gateway = DashboardSpreadsheetGateway(
        service_account=service_account,
        spreadsheet_id=config.dashboard.spreadsheet_id,
        staff_sheet_id=config.dashboard.staff_sheet_id,
        economics_sheet_id=config.dashboard.economics_sheet_id,
    )

    with sqlite3.connect("./database.db") as connection:
        storage_gateway = StorageGateway(connection=connection)
        units_economics_data = (
            storage_gateway.get_unuploaded_units_economics_data()
        )
        dashboard_spreadsheet_gateway.append_economics_data(
            units_economics_data,
        )
        storage_gateway.mark_units_economics_data_as_uploaded(
            units_economics_data,
        )


if __name__ == "__main__":
    main()
