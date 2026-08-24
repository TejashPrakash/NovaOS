from ai.skills.base import Skill, string_parameters
from ai.skills.base import SkillError


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
        # Access the NovaOS app instance through kernel
        if hasattr(kernel, 'desktop') and kernel.desktop:
            # This would need to be implemented in the desktop
            return "Premium effects toggled"
        raise SkillError("Desktop not available")
    except Exception as e:
        raise SkillError(f"Could not toggle effects: {e}")


SKILLS = (
    Skill(
        tool=string_parameters(
            name="get_theme",
            description="Get the current system theme name"
        ),
        run=get_theme
    ),
    Skill(
        tool=string_parameters(
            name="set_theme",
            description="Set the system theme",
            theme_name="Theme name to set"
        ),
        run=set_theme
    ),
    Skill(
        tool=string_parameters(
            name="toggle_premium_effects",
            description="Toggle premium visual effects on/off"
        ),
        run=toggle_premium_effects
    ),
)