"""Useful dates and times."""

from datetime import UTC, date, datetime, time

end_of_today = datetime.combine(date.today(), time.max).astimezone(UTC)
