from ai.skills.base import Skill, string_parameters
from ai.skills.base import SkillError


def open_url(kernel, url: str) -> str:
    """Open a URL in the browser."""
    try:
        # This would integrate with the browser app to open URLs
        window_manager = kernel.get_service("window_manager")
        if window_manager:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            return f"Opening {url} in browser"
        raise SkillError("Window manager not available")
    except Exception as e:
        raise SkillError(f"Could not open URL: {e}")


def search_web(kernel, query: str) -> str:
    """Search the web with a query."""
    try:
        search_url = f"https://www.google.com/search?q={query}"
        return open_url(kernel, search_url)
    except Exception as e:
        raise SkillError(f"Could not search web: {e}")


def get_current_url(kernel) -> str:
    """Get the current browser URL."""
    try:
        # This would get the active browser tab's URL
        return "Current URL feature not yet implemented"
    except Exception as e:
        raise SkillError(f"Could not get current URL: {e}")


SKILLS = [
    Skill(
        tool=string_parameters(
            name="open_url",
            description="Open a URL in the browser",
            url="The URL to open"
        ),
        run=open_url
    ),
    Skill(
        tool=string_parameters(
            name="search_web",
            description="Search the web with a query",
            query="Search query"
        ),
        run=search_web
    ),
    Skill(
        tool=string_parameters(
            name="get_current_url",
            description="Get the current browser URL"
        ),
        run=get_current_url
    ),
]