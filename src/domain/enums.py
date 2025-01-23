from enum import StrEnum


__all__ = ("StaffMemberType", "StaffMemberStatus")


class StaffMemberType(StrEnum):
    OPERATOR = "Operator"
    KITCHEN_MEMBER = "KitchenMember"
    COURIER = "Courier"
    CASHIER = "Cashier"
    PERSONAL_MANAGER = "PersonalManager"


class StaffMemberStatus(StrEnum):
    ACTIVE = "Active"
    DISMISSED = "Dismissed"
    SUSPENDED = "Suspended"
