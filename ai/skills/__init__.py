from ai.skills import apps, notes, system, weather, time_skill, calculator
from ai.skills import settings, terminal, music, file_manager, browser
from ai.skills import calendar_skill
from ai.skills.base import Skill, SkillError

# Convert all skills to tuples for consistent concatenation
SKILLS = (
    tuple(apps.SKILLS) + 
    tuple(notes.SKILLS) + 
    tuple(system.SKILLS) + 
    tuple(weather.SKILLS) + 
    tuple(time_skill.SKILLS) + 
    tuple(calculator.SKILLS) +
    tuple(settings.SKILLS) +
    tuple(terminal.SKILLS) +
    tuple(music.SKILLS) +
    tuple(file_manager.SKILLS) +
    tuple(browser.SKILLS) +
    tuple(calendar_skill.SKILLS)
)

SKILLS_BY_NAME = {skill.name: skill for skill in SKILLS}

TOOLS = tuple(skill.tool for skill in SKILLS)

__all__ = [
    "SKILLS",
    "SKILLS_BY_NAME",
    "TOOLS",
    "Skill",
    "SkillError",
    "find",
]


def find(name):
    """Return the skill with this name, or None."""
    return SKILLS_BY_NAME.get(name)