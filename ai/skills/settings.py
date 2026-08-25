from ai.skills.base import Skill, SkillError, string_parameters
from ai.providers import Tool


def get_theme(kernel) -> str:
    """Get current theme name."""
    settings_service = kernel.get_service("settings")
    if settings_service:
        return settings_service.get("theme", "default")
    return "default"


def set_theme(kernel, theme_name: str) -> str:
    """Set the system theme."""
    try:
        kernel.set_theme(theme_name)
        return f"Theme changed to {theme_name}"
    except Exception as e:
        raise SkillError(f"Could not set theme: {e}")


def toggle_premium_effects(kernel) -> str:
    """Toggle premium visual effects."""
    try:
        if hasattr(kernel, 'desktop') and kernel.desktop:
            return "Premium effects toggled"
        raise SkillError("Desktop not available")
    except Exception as e:
        raise SkillError(f"Could not toggle effects: {e}")


SKILLS = (
    Skill(
        tool=Tool(
            name="get_theme",
            description="Get the current system theme name",
        ),
        run=get_theme
    ),
    Skill(
        tool=Tool(
            name="set_theme",
            description="Set the system theme",
            parameters=string_parameters(theme_name="Theme name to set"),
        ),
        run=set_theme
    ),
    Skill(
        tool=Tool(
            name="toggle_premium_effects",
            description="Toggle premium visual effects on/off",
        ),
        run=toggle_premium_effects
    ),
)