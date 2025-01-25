from dataclasses import dataclass

import pendulum


__all__ = (
    "Period",
    "get_week_period",
    "get_weeks_count_of_month",
    "get_current_week_number",
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


def get_week_period(
    *,
    year: int,
    month: int,
    week: int,
    timezone: pendulum.Timezone,
) -> Period:
    """
    Returns the period corresponding to a specific week of the current month.

    Args:
        year (int): The year number.
        month (int): The month number (1-12).
        week (int): The week number (1-5).
        timezone (pendulum.Timezone): The timezone to consider.

    Returns:
        Period: The period representing the specified week.

    Raises:
        ValueError: If the week number is not valid (e.g., greater than 5 or less than 1).
    """
    if not (1 <= week <= 5):
        raise ValueError(f"Invalid week: {week}. Week must be between 1 and 5.")

    start_of_month = pendulum.datetime(year=year, month=month, day=1, tz=timezone)
    end_of_month = start_of_month.end_of("month")

    from_day = (week - 1) * 7 + 1
    from_date = start_of_month.add(days=from_day - 1).start_of("day")

    has_last_week_of_month_fewer_than_7_days = (
        week == 5 or from_date.add(days=6) > end_of_month
    )
    if has_last_week_of_month_fewer_than_7_days:
        to_date = end_of_month
    else:
        to_date = from_date.add(days=6).end_of("day")

    return Period(from_date=from_date, to_date=to_date)


def get_weeks_count_of_month(*, year: int, month: int) -> int:
    """
    Returns the number of weeks in the specified month.

    Args:
        year (int): The year number.
        month (int): The month number (1-12).

    Returns:
        int: The number of weeks in the specified month.
    """
    start_of_month = pendulum.datetime(year=year, month=month, day=1)
    end_of_month = start_of_month.end_of("month")

    weeks_count = 0
    current_date = start_of_month
    while current_date <= end_of_month:
        weeks_count += 1
        current_date = current_date.add(weeks=1)

    return weeks_count
