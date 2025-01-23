from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID
from zoneinfo import ZoneInfo

from infrastructure.dodo_is_api.connection import DodoIsApiConnection
from domain.services.period import Period
from domain.services.delivery import compute_orders_per_courier
from domain.entities import UnitDeliveryStatistics
from infrastructure.dodo_is_api.response_parsers import (
    parse_delivery_statistics_response,
)


__all__ = ("DeliveryStatisticsForMonthFetchInteractor",)


@dataclass(frozen=True, slots=True, kw_only=True)
class DeliveryStatisticsForMonthFetchInteractor:
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
        )
        response = self.dodo_is_api_connection.get_delivery_statistics(
            from_date=period.from_date,
            to_date=period.to_date,
            unit_uuids=self.unit_uuids,
        )
        units_delivery_statistics = parse_delivery_statistics_response(response)

        result: list[UnitDeliveryStatistics] = []

        for unit_delivery_statistics in units_delivery_statistics:
            orders_per_courier = compute_orders_per_courier(
                delivery_orders_count=unit_delivery_statistics.delivery_orders_count,
                couriers_shift_duration=unit_delivery_statistics.couriers_shifts_duration,
            )
            result.append(
                UnitDeliveryStatistics(
                    unit_uuid=unit_delivery_statistics.unit_uuid,
                    unit_name=unit_delivery_statistics.unit_name,
                    delivery_orders_count=unit_delivery_statistics.delivery_orders_count,
                    orders_per_courier=orders_per_courier,
                )
            )

        return result
