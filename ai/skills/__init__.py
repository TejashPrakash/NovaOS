"""Skill registry for the NovaOS AI layer."""

from ai.skills import apps, notes, system
from ai.skills.base import Skill, SkillError
from ai.skills import apps, notes, system, weather

SKILLS = apps.SKILLS + notes.SKILLS + system.SKILLS + weather.SKILLS

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