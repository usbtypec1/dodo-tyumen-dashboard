from dataclasses import dataclass

import pendulum


__all__ = (
    "Period",
    "get_current_week_number",
    "get_current_week_number_of_year",
    "get_month_number_by_week_number_of_year",
)


@dataclass(frozen=True, slots=True, kw_only=True)
class Period:
    from_date: pendulum.DateTime
    to_date: pendulum.DateTime

    @classmethod
    def current_month(cls, timezone: pendulum.Timezone) -> "Period":
        now = pendulum.now(timezone)
        return cls(
            from_date=now.start_of("month"),
            to_date=now.end_of("month"),
        )

    @classmethod
    def from_month(
        cls, *, month: int, year: int, timezone: pendulum.Timezone
    ) -> "Period":
        start_of_month = pendulum.datetime(year, month, 1, tz=timezone)
        end_of_month = start_of_month.end_of("month").end_of("day")
        return cls(
            from_date=start_of_month,
            to_date=end_of_month,
        )

    def rounded_to_upper_hour(self) -> "Period":
        return Period(
            from_date=self.from_date,
            to_date=self.to_date.add(hours=1).start_of("hour"),
        )


def get_current_week_number(timezone: pendulum.Timezone) -> int:
    """
    Returns the week number of the current week.

    Args:
        timezone (pendulum.Timezone): The timezone to consider.

    Returns:
        int: The week number of the current week.
    """
    now = pendulum.now(timezone)
    return (now.day - 1) // 7 + 1


def get_current_week_number_of_year(timezone: pendulum.Timezone) -> int:
    """
    Returns the week number of the current week of the year.

    Args:
        timezone (pendulum.Timezone): The timezone to consider.

    Returns:
        int: The week number of the current week of the year.
    """
    now = pendulum.now(timezone)
    return now.week_of_year


def get_period_by_week_number_of_year(
    week_number: int, year: int, timezone: pendulum.Timezone
) -> Period:
    """
    Returns the period corresponding to a specific week of the year.

    Args:
        week_number (int): The week number (1-53).
        year (int): The year number.
        timezone (pendulum.Timezone): The timezone to consider.

    Returns:
        Period: The period representing the specified week.

    Raises:
        ValueError: If the week number is not valid (e.g., greater than 53 or less than 1).
    """
    if not (1 <= week_number <= 53):
        raise ValueError(
            f"Invalid week number: {week_number}. Week number must be between 1 and 53."
        )

    start_of_year = pendulum.datetime(year=year, month=1, day=1, tz=timezone)
    from_date = start_of_year.add(weeks=week_number - 1).start_of("week")
    to_date = from_date.end_of("week")

    return Period(from_date=from_date, to_date=to_date)


def get_month_number_by_week_number_of_year(week_number: int, year: int):
    """
    Returns the month number corresponding to a specific week of the year.

    Args:
        week_number (int): The week number (1-53).
        year (int): The year number.

    Returns:
        int: The month number of the specified week.

    Raises:
        ValueError: If the week number is not valid (e.g., greater than 53 or less than 1).
    """
    if not (1 <= week_number <= 53):
        raise ValueError(
            f"Invalid week number: {week_number}. Week number must be between 1 and 53."
        )

    start_of_year = pendulum.datetime(year=year, month=1, day=1)
    week_start = start_of_year.add(weeks=week_number - 1).start_of("week")

    return week_start.month
