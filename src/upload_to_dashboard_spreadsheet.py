from fast_depends import inject

from infrastructure.dependencies.dashboard import (
    DashboardSpreadsheetGatewayDependency,
)
from infrastructure.dependencies.storage import StorageGatewayDependency


@inject
def main(
    dashboard_spreadsheet_gateway: DashboardSpreadsheetGatewayDependency,
    storage_gateway: StorageGatewayDependency,
):
    units_economics_data = storage_gateway.get_unuploaded_units_economics_data()
    dashboard_spreadsheet_gateway.append_economics_data(
        units_economics_data,
    )
    storage_gateway.mark_units_economics_data_as_uploaded(
        units_economics_data,
    )

    units_staff_data = storage_gateway.get_unuploaded_staff_data()
    dashboard_spreadsheet_gateway.append_staff_data(units_staff_data)
    storage_gateway.mark_units_staff_data_as_uploaded(units_staff_data)


if __name__ == "__main__":
    main()  # type: ignore[reportCallIssue]
