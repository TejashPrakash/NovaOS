"""AI skill for Calendar — create and query events via natural language."""

import json
from datetime import datetime
from pathlib import Path

from ai.skills.base import Skill, SkillError, string_parameters
from ai.providers import Tool


EVENTS_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "calendar_events.json"


def _load_events():
    try:
        if EVENTS_FILE.exists():
            with open(EVENTS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_events(events):
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)


def create_event(kernel, date: str, title: str, time: str = "", color: str = "#00E5FF") -> str:
    """Create a calendar event."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise SkillError(f"Invalid date format: {date}. Use YYYY-MM-DD.")

    if not title.strip():
        raise SkillError("Event title cannot be empty.")

    events = _load_events()
    event = {"title": title.strip(), "time": time.strip(), "color": color}
    events.setdefault(date, []).append(event)
    _save_events(events)

    time_str = f" at {time}" if time else ""
    return f"Created event '{title}' on {date}{time_str}"


def query_events(kernel, date: str = "") -> str:
    """Query events for a specific date or today."""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    events = _load_events()
    day_events = events.get(date, [])

    if not day_events:
        return f"No events on {date}."

    lines = [f"Events on {date}:"]
    for i, ev in enumerate(day_events, 1):
        time_str = ev.get("time", "")
        title = ev.get("title", "Untitled")
        prefix = f"{time_str} - " if time_str else ""
        lines.append(f"  {i}. {prefix}{title}")

    return "\n".join(lines)


def delete_event(kernel, date: str, title: str) -> str:
    """Delete an event by date and title."""
    events = _load_events()
    day_events = events.get(date, [])

    for i, ev in enumerate(day_events):
        if ev.get("title", "").lower() == title.lower():
            day_events.pop(i)
            if not day_events:
                del events[date]
            _save_events(events)
            return f"Deleted event '{title}' on {date}"

    raise SkillError(f"No event '{title}' found on {date}")


SKILLS = (
    Skill(
        tool=Tool(
            name="create_calendar_event",
            description="Create a calendar event with date, title, and optional time",
            parameters=string_parameters(
                date="Date in YYYY-MM-DD format",
                title="Event title",
                time="Event time (optional, e.g. 14:30)",
                color="Event color hex (optional)"
            ),
        ),
        run=create_event
    ),
    Skill(
        tool=Tool(
            name="query_calendar_events",
            description="Query calendar events for a date (defaults to today)",
            parameters=string_parameters(
                date="Date in YYYY-MM-DD format (optional, defaults to today)"
            ),
        ),
        run=query_events
    ),
    Skill(
        tool=Tool(
            name="delete_calendar_event",
            description="Delete a calendar event by date and title",
            parameters=string_parameters(
                date="Date in YYYY-MM-DD format",
                title="Exact title of the event to delete"
            ),
        ),
        run=delete_event
    ),
)
