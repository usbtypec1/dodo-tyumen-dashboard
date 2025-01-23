from uuid import UUID
from dataclasses import dataclass


__all__ = (
    "Unit",
    "UnitWeeklyStaffData",
    "UnitMonthlyEconomicsData",
    "UnitMonthlyGoals",
    "UnitDeliveryStatistics",
    "UnitMonthlySales",
    "UnitStaffCountByPosition",
)


@dataclass(slots=True, kw_only=True)
class Unit:
    uuid: UUID
    name: str


@dataclass(slots=True, kw_only=True)
class UnitMonthlySales:
    unit_uuid: UUID
    sales: int


@dataclass(slots=True, kw_only=True)
class UnitProductivityStatistics:
    unit_uuid: UUID
    unit_name: str
    sales_per_labor_hour: float


@dataclass(slots=True, kw_only=True)
class UnitMonthlyGoals:
    unit_uuid: UUID
    sales_per_person: float
    orders_per_courier: float


@dataclass(slots=True, kw_only=True)
class UnitDeliveryStatistics:
    unit_uuid: UUID
    unit_name: str
    delivery_orders_count: int
    orders_per_courier: float


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitMonthlyEconomicsData:
    unit_name: str
    year: int
    month: int
    sales: int
    delivery_orders_count: int
    sales_per_person: float
    orders_per_courier: float


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitWeeklyStaffData:
    unit_name: str
    year: int
    month: int
    week: int
    active_managers_count: int
    dismissed_managers_count: int
    active_kitchen_members_count: int
    dismissed_kitchen_members_count: int
    active_couriers_count: int
    dismissed_couriers_count: int
    active_candidates_count: int
    dismissed_candidates_count: int
    new_specialists_count: int
    active_interns_count: int
    dismissed_interns_count: int
    new_candidates_count: int


@dataclass(slots=True, kw_only=True)
class UnitStaffCountByPosition:
    unit_uuid: UUID
    managers_count: int
    kitchen_members_count: int
    couriers_count: int
    candidates_count: int
    interns_count: int
