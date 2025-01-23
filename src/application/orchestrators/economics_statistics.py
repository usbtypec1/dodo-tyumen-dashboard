from collections.abc import Iterable
from dataclasses import dataclass

from application.interactors.delivery_statistics_fetch import (
    DeliveryStatisticsForMonthFetchInteractor,
)
from application.interactors.monthly_sales_fetch import MonthlySalesFetchInteractor
from application.interactors.productivity_statistics_fetch import (
    ProductivityStatisticsForMonthFetchInteractor,
)
from application.interactors.unit_monthly_goals_fetch import (
    UnitMonthlyGoalsFetchInteractor,
)
from bootstrap.logger import create_logger
from domain.entities import Unit, UnitMonthlyEconomicsData
from domain.services.units import map_unit_uuid_to_item


logger = create_logger("orchestrators")


__all__ = ("EconomicsStatisticsOrchestrator",)


@dataclass(frozen=True, slots=True, kw_only=True)
class EconomicsStatisticsOrchestrator:
    units: Iterable[Unit]
    month: int
    year: int
    delivery_statistics_fetch_interactor: DeliveryStatisticsForMonthFetchInteractor
    produciton_statistics_fetch_interactor: (
        ProductivityStatisticsForMonthFetchInteractor
    )
    unit_monthly_goals_fetch_intetactors: Iterable[UnitMonthlyGoalsFetchInteractor]
    monthly_sales_fetch_interactor: MonthlySalesFetchInteractor

    def execute(self):
        production_statistics = self.produciton_statistics_fetch_interactor.execute()
        delivery_statistics = self.delivery_statistics_fetch_interactor.execute()
        monthly_sales = self.monthly_sales_fetch_interactor.execute()

        units_monthly_goals = []
        for (
            unit_monthly_goals_fetch_intetactor
        ) in self.unit_monthly_goals_fetch_intetactors:
            unit_monthly_goals = unit_monthly_goals_fetch_intetactor.execute()
            units_monthly_goals.append(unit_monthly_goals)

        unit_uuid_to_delivery_statistics = map_unit_uuid_to_item(delivery_statistics)
        unit_uuid_to_productivity_statistics = map_unit_uuid_to_item(
            production_statistics
        )
        unit_uuid_to_monthly_sales = map_unit_uuid_to_item(monthly_sales)
        unit_uuid_to_monthly_goals = map_unit_uuid_to_item(units_monthly_goals)

        units_economics_data: list[UnitMonthlyEconomicsData] = []

        for unit in self.units:
            unit_delivery_statistics = unit_uuid_to_delivery_statistics.get(unit.uuid)
            unit_productivity_statistics = unit_uuid_to_productivity_statistics.get(
                unit.uuid
            )
            unit_monthly_sales = unit_uuid_to_monthly_sales.get(unit.uuid)
            unit_monthly_goals = unit_uuid_to_monthly_goals.get(unit.uuid)

            sales = 0
            if unit_monthly_sales is not None:
                sales = unit_monthly_sales.sales

            sales_per_person = 0
            orders_per_courier = 0

            if unit_monthly_goals is not None:
                sales_per_person = unit_monthly_goals.sales_per_person
                orders_per_courier = unit_monthly_goals.orders_per_courier

            delivery_orders_count = 0
            if unit_delivery_statistics is not None:
                delivery_orders_count = unit_delivery_statistics.delivery_orders_count

            if unit_productivity_statistics is not None and sales_per_person == 0:
                sales_per_person = unit_productivity_statistics.sales_per_labor_hour

            unit_monthly_economics_data = UnitMonthlyEconomicsData(
                unit_name=unit.name,
                month=self.month,
                year=self.year,
                sales=sales,
                delivery_orders_count=delivery_orders_count,
                sales_per_person=sales_per_person,
                orders_per_courier=orders_per_courier,
            )
            units_economics_data.append(unit_monthly_economics_data)

        return units_economics_data
