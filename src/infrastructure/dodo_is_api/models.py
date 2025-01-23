from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field

from domain.enums import StaffMemberStatus, StaffMemberType


__all__ = (
    "UnitDeliveryStatistics",
    "UnitProductivityStatistics",
    "UnitMonthlyGoals",
    "UnitMonthlySales",
    "StaffMember",
    "StaffMembersResponse",
)


class UnitDeliveryStatistics(BaseModel):
    unit_uuid: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    delivery_orders_count: Annotated[
        int, Field(validation_alias="deliveryOrdersCount")
    ]
    couriers_shifts_duration: Annotated[
        int, Field(validation_alias="couriersShiftsDuration")
    ]


class UnitProductivityStatistics(BaseModel):
    unit_uuid: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    sales_per_labor_hour: Annotated[
        float, Field(validation_alias="salesPerLaborHour")
    ]


class UnitMonthlyGoals(BaseModel):
    sales_per_person: Annotated[float, Field(validation_alias="salesPerPerson")]
    orders_per_courier: Annotated[
        float, Field(validation_alias="ordersPerCourier")
    ]


class UnitMonthlySales(BaseModel):
    unit_uuid: Annotated[UUID, Field(validation_alias="unitId")]
    sales: int


class StaffMember(BaseModel):
    id: str
    first_name: Annotated[str, Field(validation_alias="firstName")]
    last_name: Annotated[str, Field(validation_alias="lastName")]
    patronymic_name: Annotated[
        str | None, Field(validation_alias="patronymicName")
    ]
    unit_uuid: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    staff_type: Annotated[StaffMemberType, Field(validation_alias="staffType")]
    position_id: Annotated[UUID, Field(validation_alias="positionId")]
    position_name: Annotated[str, Field(validation_alias="positionName")]
    status: StaffMemberStatus
    dismissed_on: Annotated[str | None, Field(validation_alias="dismissedOn")]


class StaffMembersResponse(BaseModel):
    members: list[StaffMember]
    skipped_count: Annotated[int, Field(validation_alias="skippedCount")]
    taken_count: Annotated[int, Field(validation_alias="takenCount")]
    total_count: Annotated[int, Field(validation_alias="totalCount")]
    is_end_of_list_reached: Annotated[
        bool, Field(validation_alias="isEndOfListReached")
    ]
