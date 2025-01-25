from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

import pendulum

from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from domain.services.period import Period
from domain.entities import UnitMonthlySales
from infrastructure.dodo_is_api.response_parsers import (
    parse_monthly_sales_response,
)


__all__ = ("MonthlySalesFetchInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class MonthlySalesFetchInteractor:
    dodo_is_api_connection: DodoIsApiConnection
    month: int
    year: int
    timezone: pendulum.Timezone
    unit_uuids: Iterable[UUID]

    def execute(self):
        period = Period.from_month(
            month=self.month,
            year=self.year,
            timezone=self.timezone,
        )
        response = self.dodo_is_api_connection.get_monthly_units_sales(
            from_date=period.from_date,
            to_date=period.to_date,
            unit_uuids=self.unit_uuids,
        )
        monthly_sales = parse_monthly_sales_response(response)
        return [
            UnitMonthlySales(
                unit_uuid=unit_monthly_sales.unit_uuid,
                sales=unit_monthly_sales.sales,
            )
            for unit_monthly_sales in monthly_sales
        ]
