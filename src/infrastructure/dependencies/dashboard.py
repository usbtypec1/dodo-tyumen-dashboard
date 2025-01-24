from typing import Annotated

from fast_depends import Depends
from infrastructure.dashboard import DashboardSpreadsheetGateway
from infrastructure.dependencies.config import ConfigDependency
from infrastructure.dependencies.service_account import ServiceAccountDependency


__all__ = (
    "get_dashboard_spreadsheet_gateway",
    "DashboardSpreadsheetGatewayDependency",
)


def get_dashboard_spreadsheet_gateway(
    service_account: ServiceAccountDependency,
    config: ConfigDependency,
) -> DashboardSpreadsheetGateway:
    return DashboardSpreadsheetGateway(
        service_account=service_account,
        spreadsheet_id=config.dashboard.spreadsheet_id,
        staff_sheet_id=config.dashboard.staff_sheet_id,
        economics_sheet_id=config.dashboard.economics_sheet_id,
    )


DashboardSpreadsheetGatewayDependency = Annotated[
    DashboardSpreadsheetGateway, Depends(get_dashboard_spreadsheet_gateway)
]
