"""Time and date skill for NovaOS AI layer."""

from datetime import datetime
import pytz
from ai.skills.base import Skill, string_parameters
from ai.providers import Tool


def get_current_time(kernel, timezone: str = "UTC") -> str:
    """Get current time for a specific timezone."""
    
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"Current time in {timezone}: {now.strftime('%I:%M %p')}"
    except Exception:
        return f"Unknown timezone: {timezone}. Available: UTC, America/New_York, Europe/London, etc."


def get_current_date(kernel) -> str:
    """Get current date."""
    
    now = datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}"


def get_datetime_info(kernel, timezone: str = "UTC") -> str:
    """Get complete date and time information."""
    
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return f"Date: {now.strftime('%A, %B %d, %Y')}. Time: {now.strftime('%I:%M:%S %p')} in {timezone}"
    except Exception:
        return f"Could not get time for timezone: {timezone}"


SKILLS = (
    Skill(
        tool=Tool(
            name="get_current_time",
            description="Get current time for a specific timezone.",
            parameters=string_parameters(
                timezone="Timezone name, e.g. UTC, America/New_York, Europe/London"
            ),
        ),
        run=get_current_time,
    ),
    Skill(
        tool=Tool(
            name="get_current_date",
            description="Get current date.",
        ),
        run=get_current_date,
    ),
    Skill(
        tool=Tool(
            name="get_datetime_info",
            description="Get complete date and time information.",
            parameters=string_parameters(
                timezone="Timezone name (defaults to UTC)"
            ),
        ),
        run=get_datetime_info,
    ),
)