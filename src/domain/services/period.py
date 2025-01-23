from dataclasses import dataclass

import pendulum


__all__ = ("Period", "get_weeks_of_month", "get_week_period")


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


def get_weeks_of_month(
    *,
    month: int,
    year: int,
    timezone: pendulum.Timezone,
) -> list[Period]:
    """
    Returns periods representing the weeks of a specific month.

    Each week is defined as:
    - Week 1: 1st to 7th
    - Week 2: 8th to 14th
    - Week 3: 15th to 21st
    - Week 4: 22nd to 28th
    - Week 5: 29th to the end of the month (except non-leap year on february).

    Args:
        month (int): The month (1-12).
        year (int): The year.
        timezone (pendulum.Timezone): The timezone for the periods.

    Returns:
        list[Period]: List of weekly periods for the specified month.
    """
    month_period = Period.from_month(month=month, year=year, timezone=timezone)
    from_date = month_period.from_date
    to_date = month_period.to_date

    weeks = []
    current_start = from_date

    while current_start <= to_date:
        current_end = min(current_start.add(days=6).end_of("day"), to_date)
        weeks.append(Period(from_date=current_start, to_date=current_end))
        current_start = current_end.add(days=1).start_of("day")

    return weeks


def get_current_week_of_month(timezone: pendulum.Timezone) -> int:
    """
    Returns the current week number within the month for the given timezone.

    Args:
        timezone (pendulum.Timezone): The timezone to consider.

    Returns:
        int: The current week number of the month.
    """
    now = pendulum.now(timezone)
    return ((now.day - 1) // 7) + 1


def get_current_week_period(timezone: pendulum.Timezone) -> Period:
    """
    Returns the period representing the current week for the given timezone.

    Args:
        timezone (pendulum.Timezone): The timezone to consider.

    Returns:
        Period: The period representing the current week.
    """
    now = pendulum.now(timezone)
    start_of_week = now.start_of("week")
    end_of_week = now.end_of("week")
    return Period(from_date=start_of_week, to_date=end_of_week)


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
    
    has_last_week_of_month_fewer_than_7_days = week == 5 or from_date.add(days=6) > end_of_month
    if has_last_week_of_month_fewer_than_7_days:
        to_date = end_of_month
    else:
        to_date = from_date.add(days=6).end_of("day")

    return Period(from_date=from_date, to_date=to_date)
