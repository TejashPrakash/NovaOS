from urllib.parse import quote_plus
from ai.skills.base import Skill, string_parameters, SkillError
from ai.providers import Tool


def open_url(kernel, url: str) -> str:
    """Open a URL in the browser.

    Thread-safe: all tkinter calls are scheduled on the main thread
    via root.after() because AI skills run in a background thread.
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Get root window for thread-safe scheduling
        root = None
        if hasattr(kernel, 'desktop') and kernel.desktop:
            root = getattr(kernel.desktop, 'root', None)

        process_manager = kernel.get_service("process_manager")
        if process_manager:
            process = process_manager.get_process("Browser")
            if process and process.instance:
                app = process.instance

                def _navigate():
                    """Navigate the browser to the URL (runs on main thread)."""
                    try:
                        if hasattr(app, 'current_tab') and app.current_tab:
                            app.controller.navigate(app.current_tab, url)
                            app.toolbar.set_url(url)
                            app.show_browser()
                            app.update_current_tab(url, url)
                            app.update_navigation()
                    except Exception as e:
                        print(f"[Browser] Navigate error: {e}")

                if root:
                    root.after(0, _navigate)
                else:
                    _navigate()
                return f"Opened {url} in browser"

        # No browser open — launch it, then navigate
        def _launch_and_navigate():
            try:
                process = process_manager.start_process("Browser")
                if process and process.instance:
                    app = process.instance
                    # Wait a moment for the browser to initialize
                    def _do_nav():
                        try:
                            if hasattr(app, 'current_tab') and app.current_tab:
                                app.controller.navigate(app.current_tab, url)
                                app.toolbar.set_url(url)
                                app.show_browser()
                                app.update_current_tab(url, url)
                                app.update_navigation()
                        except Exception as e:
                            print(f"[Browser] Post-launch navigate error: {e}")
                    if root:
                        root.after(500, _do_nav)
            except Exception as e:
                print(f"[Browser] Launch error: {e}")

        if root:
            root.after(0, _launch_and_navigate)
        return f"Browser opened. Navigating to {url}"
    except SkillError:
        raise
    except Exception as e:
        raise SkillError(f"Could not open URL: {e}")


def search_web(kernel, query: str) -> str:
    """Search the web with a query."""
    try:
        search_url = f"https://www.google.com/search?q={quote_plus(query)}"
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