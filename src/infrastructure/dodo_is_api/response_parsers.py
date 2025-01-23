import json
from typing import Any

import httpx
from pydantic import TypeAdapter, ValidationError

from infrastructure.exceptions.response_parsers import (
    ResponseStatusCodeError,
    ResponseJsonParseError,
    ResponseJsonInvalidTypeError,
    ResponseDataParseError,
)
from infrastructure.dodo_is_api.models import (
    StaffMembersResponse,
    UnitDeliveryStatistics,
    UnitProductivityStatistics,
    UnitMonthlyGoals,
    UnitMonthlySales,
    StaffPositionsHistoryResponse,
)


__all__ = (
    "parse_response_json",
    "ensure_response_data_is_dict",
    "ensure_response_data_is_list",
    "parse_delivery_statistics_response",
    "parse_productivity_statistics_response",
    "parse_monthly_sales_response",
    "parse_staff_members_response",
    "parse_staff_positions_history_response",
)


def parse_response_json(response: httpx.Response) -> dict | list:
    try:
        return response.json()
    except json.JSONDecodeError as error:
        raise ResponseJsonParseError(response=response) from error


def ensure_response_data_is_dict(response_data: Any) -> dict:
    if not isinstance(response_data, dict):
        raise ResponseJsonInvalidTypeError
    return response_data


def ensure_response_data_is_list(response_data: Any) -> list:
    if not isinstance(response_data, list):
        raise ResponseJsonInvalidTypeError
    return response_data


def ensure_status_code_success(response: httpx.Response) -> None:
    if not response.is_success:
        raise ResponseStatusCodeError(response=response)


def parse_delivery_statistics_response(
    response: httpx.Response,
) -> list[UnitDeliveryStatistics]:
    """
    Parses the response for delivery statistics.

    Args:
        response (httpx.Response): The HTTP response object.

    Returns:
        list[UnitProductivityStatistics]: A list of delivery statistics objects.

    Raises:
        ResponseStatusCodeError: If the response status code indicates failure.
        ResponseJsonParseError: If the response JSON is invalid.
        ResponseJsonInvalidTypeError: If the response data type is not valid.
        ResponseDataParseError: If the expected data structure is missing or invalid.
    """
    ensure_status_code_success(response)

    response_data: dict | list = parse_response_json(response)

    response_data = ensure_response_data_is_dict(response_data)

    try:
        units_delivery_statistics = response_data["unitsStatistics"]
    except KeyError as error:
        raise ResponseDataParseError(response_data=response_data) from error

    type_adapter = TypeAdapter(list[UnitDeliveryStatistics])

    try:
        return type_adapter.validate_python(units_delivery_statistics)
    except ValidationError as error:
        raise ResponseDataParseError(response_data=response_data) from error


def parse_productivity_statistics_response(
    response: httpx.Response,
) -> list[UnitProductivityStatistics]:
    """
    Parses the response for productivity statistics.

    Args:
        response (httpx.Response): The HTTP response object.

    Returns:
        list[UnitProductivityStatistics]: A list of productivity statistics objects.

    Raises:
        ResponseStatusCodeError: If the response status code indicates failure.
        ResponseJsonParseError: If the response JSON is invalid.
        ResponseJsonInvalidTypeError: If the response data type is not valid.
        ResponseDataParseError: If the expected data structure is missing or invalid.
    """
    ensure_status_code_success(response)

    response_data: dict | list = parse_response_json(response)

    response_data = ensure_response_data_is_dict(response_data)

    try:
        productivity_statistics = response_data["productivityStatistics"]
    except KeyError as error:
        raise ResponseDataParseError(response_data=response_data) from error

    type_adapter = TypeAdapter(list[UnitProductivityStatistics])

    try:
        return type_adapter.validate_python(productivity_statistics)
    except ValidationError as error:
        raise ResponseDataParseError(response_data=response_data) from error


def parse_unit_monthly_goals_response(
    response: httpx.Response,
) -> UnitMonthlyGoals:
    """
    Parses the response for unit monthly goals.

    Args:
        response (httpx.Response): The HTTP response object.

    Returns:
        UnitMonthlyGoals: Parsed unit monthly goals object.

    Raises:
        ResponseStatusCodeError: If the response status code indicates failure.
        ResponseJsonParseError: If the response JSON is invalid.
        ResponseJsonInvalidTypeError: If the response data type is not valid.
        ResponseDataParseError: If the expected data structure is missing or invalid.
    """
    ensure_status_code_success(response)

    response_data = parse_response_json(response)

    try:
        return UnitMonthlyGoals.model_validate(response_data)
    except ValidationError as error:
        raise ResponseDataParseError(response_data=response_data) from error


def parse_monthly_sales_response(
    response: httpx.Response,
) -> list[UnitMonthlySales]:
    """
    Parses the response for monthly sales.

    Args:
        response (httpx.Response): The HTTP response object.

    Returns:
        List[MonthlySales]: A list of parsed monthly sales objects.

    Raises:
        ResponseStatusCodeError: If the response status code indicates failure.
        ResponseJsonParseError: If the response JSON is invalid.
        ResponseJsonInvalidTypeError: If the response data type is not valid.
        ResponseDataParseError: If the expected data structure is missing or invalid.
    """
    ensure_status_code_success(response)

    response_data: Any = parse_response_json(response)

    response_data = ensure_response_data_is_dict(response_data)

    try:
        result = response_data["result"]
    except KeyError as error:
        raise ResponseDataParseError(response_data=response_data) from error

    type_adapter = TypeAdapter(list[UnitMonthlySales])

    try:
        return type_adapter.validate_python(result)
    except ValidationError as error:
        raise ResponseDataParseError(response_data=response_data) from error


def parse_staff_members_response(
    response: httpx.Response,
) -> StaffMembersResponse:
    """
    Parses the response for staff members.

    Args:
        response (httpx.Response): The HTTP response object.

    Returns:
        MembersResponse: Parsed members response object.

    Raises:
        ResponseStatusCodeError: If the response status code indicates failure.
        ResponseJsonParseError: If the response JSON is invalid.
        ResponseJsonInvalidTypeError: If the response data type is not valid.
        ResponseDataParseError: If the expected data structure is missing or invalid.
    """
    ensure_status_code_success(response)

    response_data: Any = parse_response_json(response)

    response_data = ensure_response_data_is_dict(response_data)

    try:
        return StaffMembersResponse.model_validate(response_data)
    except ValidationError as error:
        raise ResponseDataParseError(response_data=response_data) from error


def parse_staff_positions_history_response(
    response: httpx.Response,
) -> StaffPositionsHistoryResponse:
    """
    Parses the response for staff positions history.

    Args:
        response (httpx.Response): The HTTP response object.

    Returns:
        MembersResponse: Parsed staff positions history response object.

    Raises:
        ResponseStatusCodeError: If the response status code indicates failure.
        ResponseJsonParseError: If the response JSON is invalid.
        ResponseJsonInvalidTypeError: If the response data type is not valid.
        ResponseDataParseError: If the expected data structure is missing or invalid.
    """
    ensure_status_code_success(response)

    response_data: Any = parse_response_json(response)

    response_data = ensure_response_data_is_dict(response_data)

    try:
        return StaffPositionsHistoryResponse.model_validate(response_data)
    except ValidationError as error:
        raise ResponseDataParseError(response_data=response_data) from error
