from ai.skills.base import Skill, string_parameters, SkillError
from ai.providers import Tool


def open_url(kernel, url: str) -> str:
    """Open a URL in the browser."""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Try to open in existing browser tab
        process_manager = kernel.get_service("process_manager")
        if process_manager:
            process = process_manager.get_process("Browser")
            if process and process.instance:
                app = process.instance
                if hasattr(app, 'current_tab') and app.current_tab:
                    app.controller.navigate(app.current_tab, url)
                    app.toolbar.set_url(url)
                    app.show_browser()
                    app.update_current_tab(url, url)
                    app.update_navigation()
                    return f"Opened {url} in browser"

        # No browser open — launch it
        process_manager.start_process("Browser")
        return f"Browser opened. Navigating to {url}"
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