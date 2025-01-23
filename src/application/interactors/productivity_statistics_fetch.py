from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID
from zoneinfo import ZoneInfo

from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from domain.services.period import Period
from domain.entities import UnitProductivityStatistics
from infrastructure.dodo_is_api.response_parsers import (
    parse_productivity_statistics_response,
)


__all__ = ("ProductivityStatisticsForMonthFetchInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductivityStatisticsForMonthFetchInteractor:
    dodo_is_api_connection: DodoIsApiConnection
    month: int
    year: int
    timezone: ZoneInfo
    unit_uuids: Iterable[UUID]

    def execute(self):
        period = Period.from_month(
            month=self.month,
            year=self.year,
            timezone=self.timezone,
        ).rounded_to_upper_hour()
        
        response = self.dodo_is_api_connection.get_production_productivity(
            from_date=period.from_date,
            to_date=period.to_date,
            unit_uuids=self.unit_uuids,
        )
        units_productivity_statistics = parse_productivity_statistics_response(
            response
        )
        return [
            UnitProductivityStatistics(
                unit_uuid=unit_productivity_statistics.unit_uuid,
                unit_name=unit_productivity_statistics.unit_name,
                sales_per_labor_hour=unit_productivity_statistics.sales_per_labor_hour,
            )
            for unit_productivity_statistics in units_productivity_statistics
        ]
