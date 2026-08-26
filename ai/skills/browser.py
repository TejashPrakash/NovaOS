from ai.skills.base import Skill, string_parameters, SkillError
from ai.providers import Tool


def open_url(kernel, url: str) -> str:
    """Open a URL in the browser."""
    try:
        window_manager = kernel.get_service("window_manager")
        if window_manager:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            return f"Opening {url} in browser"
        raise SkillError("Window manager not available")
    except SkillError:
        raise
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
        process_manager = kernel.get_service("process_manager")
        if process_manager:
            process = process_manager.get_process("Browser")
            if process and process.instance:
                app = process.instance
                if hasattr(app, "current_tab") and app.current_tab:
                    url = app.current_tab.url
                    if url and url != "about:home":
                        return f"Current URL: {url}"
                    return "Browser is on the homepage"
            return "Browser is not open"
        raise SkillError("Process manager not available")
    except SkillError:
        raise
    except Exception as e:
        raise SkillError(f"Could not get current URL: {e}")


SKILLS = (
    Skill(
        tool=Tool(
            name="open_url",
            description="Open a URL in the browser",
            parameters=string_parameters(url="The URL to open"),
        ),
        run=open_url
    ),
    Skill(
        tool=Tool(
            name="search_web",
            description="Search the web with a query",
            parameters=string_parameters(query="Search query"),
        ),
        run=search_web
    ),
    Skill(
        tool=Tool(
            name="get_current_url",
            description="Get the current browser URL",
        ),
        run=get_current_url
    ),
)