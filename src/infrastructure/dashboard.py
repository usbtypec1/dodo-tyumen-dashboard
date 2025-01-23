from collections.abc import Iterable

from gspread.client import Client

from domain.entities import UnitMonthlyEconomicsData, UnitWeeklyStaffData


__all__ = ("DashboardSpreadsheetGateway",)


class DashboardSpreadsheetGateway:
    def __init__(
        self,
        *,
        service_account: Client,
        spreadsheet_id: str,
        staff_sheet_id: int,
        economics_sheet_id: int,
    ) -> None:
        self.__spreadsheet = service_account.open_by_key(spreadsheet_id)
        self.__staff_sheet = self.__spreadsheet.get_worksheet_by_id(
            staff_sheet_id
        )
        self.__economics_sheet = self.__spreadsheet.get_worksheet_by_id(
            economics_sheet_id
        )

    def append_staff_data(
        self, units_data: Iterable[UnitWeeklyStaffData]
    ) -> None:
        rows = [
            (
                unit_data.unit_name,
                unit_data.year,
                unit_data.month,
                unit_data.week,
                unit_data.active_managers_count,
                unit_data.dismissed_managers_count,
                unit_data.active_kitchen_members_count,
                unit_data.dismissed_kitchen_members_count,
                unit_data.active_couriers_count,
                unit_data.dismissed_couriers_count,
                unit_data.active_candidates_count,
                unit_data.new_specialists_count,
                unit_data.dismissed_candidates_count,
                unit_data.active_interns_count,
                unit_data.new_candidates_count,
                unit_data.dismissed_interns_count,
            )
            for unit_data in units_data
        ]
        self.__staff_sheet.append_rows(rows)

    def append_economics_data(
        self,
        units_data: Iterable[UnitMonthlyEconomicsData],
    ) -> None:
        rows = [
            (
                unit_data.unit_name,
                unit_data.year,
                unit_data.month,
                unit_data.sales,
                unit_data.delivery_orders_count,
                unit_data.sales_per_person,
                unit_data.orders_per_courier,
            )
            for unit_data in units_data
        ]
        self.__economics_sheet.append_rows(rows)
