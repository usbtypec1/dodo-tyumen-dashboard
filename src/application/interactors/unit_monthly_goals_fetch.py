from dataclasses import dataclass
from uuid import UUID

from domain.entities import UnitMonthlyGoals
from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from infrastructure.dodo_is_api.response_parsers import (
    parse_unit_monthly_goals_response,
)


__all__ = ("UnitMonthlyGoalsFetchInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitMonthlyGoalsFetchInteractor:
    dodo_is_api_connection: DodoIsApiConnection
    month: int
    year: int
    unit_uuid: UUID

    def execute(self):
        response = self.dodo_is_api_connection.get_unit_monthly_goals(
            month=self.month,
            year=self.year,
            unit_uuid=self.unit_uuid,
        )
        unit_month_goals = parse_unit_monthly_goals_response(response)
        return UnitMonthlyGoals(
            unit_uuid=self.unit_uuid,
            sales_per_person=unit_month_goals.sales_per_person,
            orders_per_courier=unit_month_goals.orders_per_courier,
        )
