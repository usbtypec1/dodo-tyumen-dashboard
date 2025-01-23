import datetime
from dataclasses import dataclass
from collections.abc import Iterable
from uuid import UUID

import httpx

from domain.enums import StaffMemberStatus, StaffMemberType
from infrastructure.dodo_is_api.http_client import DodoIsApiHttpClient


__all__ = ("DodoIsApiConnection", "join_uuids_with_comma", "join_with_comma")


def join_uuids_with_comma(uuids: Iterable[UUID]) -> str:
    return ",".join(uuid.hex for uuid in uuids)


def join_with_comma(items: Iterable[str]) -> str:
    return ",".join(items)


@dataclass(frozen=True, slots=True, kw_only=True)
class DodoIsApiConnection:
    http_client: DodoIsApiHttpClient

    def get_monthly_units_sales(
        self,
        *,
        from_date: datetime.date,
        to_date: datetime.date,
        unit_uuids: Iterable[UUID],
    ) -> httpx.Response:
        url = "/finances/sales/units/monthly"
        query_params = {
            "fromDate": f"{from_date:%Y-%m-%d}",
            "toDate": f"{to_date:%Y-%m-%d}",
            "units": join_uuids_with_comma(unit_uuids),
        }
        return self.http_client.get(url, params=query_params)

    def get_unit_monthly_goals(
        self,
        *,
        month: int,
        year: int,
        unit_uuid: UUID,
    ) -> httpx.Response:
        url = "/units/month-goals"
        query_params = {
            "year": year,
            "month": month,
            "unit": unit_uuid.hex,
        }
        return self.http_client.get(url, params=query_params)

    def get_delivery_statistics(
        self,
        *,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_uuids: Iterable[UUID],
    ) -> httpx.Response:
        url = "/delivery/statistics"
        query_params = {
            "from": f"{from_date:%Y-%m-%d %H:%M:%S}",
            "to": f"{to_date:%Y-%m-%d %H:%M:%S}",
            "units": join_uuids_with_comma(unit_uuids),
        }
        return self.http_client.get(url, params=query_params)

    def get_production_productivity(
        self,
        *,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_uuids: Iterable[UUID],
    ) -> httpx.Response:
        url = "/production/productivity"
        query_params = {
            "from": f"{from_date:%Y-%m-%d %H:%M:%S}",
            "to": f"{to_date:%Y-%m-%d %H:%M:%S}",
            "units": join_uuids_with_comma(unit_uuids),
        }
        return self.http_client.get(url, params=query_params)

    def get_staff_members(
        self,
        *,
        unit_uuids: Iterable[UUID] | None = None,
        take: int | None = None,
        skip: int | None = None,
        statuses: Iterable[StaffMemberStatus] | None = None,
        staff_types: Iterable[StaffMemberType] | None = None,
        dismissed_from_date: datetime.datetime | None = None,
        dismissed_to_date: datetime.datetime | None = None,
    ) -> httpx.Response:
        url = "/staff/members"
        query_params = {}
        if unit_uuids is not None:
            query_params["units"] = join_uuids_with_comma(unit_uuids)
        if take is not None:
            query_params["take"] = take
        if skip is not None:
            query_params["skip"] = skip
        if statuses is not None:
            query_params["statuses"] = join_with_comma(statuses)
        if staff_types is not None:
            query_params["staffType"] = join_with_comma(staff_types)
        if dismissed_from_date is not None:
            query_params["dismissedFrom"] = f"{dismissed_from_date:%Y-%m-%d}"
        if dismissed_to_date is not None:
            query_params["dismissedTo"] = f"{dismissed_to_date:%Y-%m-%d}"
        return self.http_client.get(url, params=query_params)
