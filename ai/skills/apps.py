"""Skills that drive NovaOS applications through the kernel command registry."""

from ai.providers import Tool
from ai.skills.base import Skill, SkillError, string_parameters


def open_app(kernel, app_name: str = "") -> str:
    """Open an app. Thread-safe: schedules tkinter calls on the main thread."""
    if not app_name:
        raise SkillError("open_app needs an app_name")

    # Schedule on main thread to avoid tkinter crash
    def _do_open():
        try:
            kernel.commands.execute(kernel, "open_app", app_name)
        except Exception:
            pass

    root = None
    if hasattr(kernel, 'desktop') and kernel.desktop and hasattr(kernel.desktop, 'root'):
        root = kernel.desktop.root
    if root:
        root.after(0, _do_open)
    else:
        kernel.commands.execute(kernel, "open_app", app_name)

    return f"Opened {app_name}."


def close_app(kernel, app_name: str = "") -> str:
    """Close an app. Thread-safe: schedules tkinter calls on the main thread."""
    if not app_name:
        raise SkillError("close_app needs an app_name")

    def _do_close():
        try:
            kernel.commands.execute(kernel, "close_app", app_name)
        except Exception:
            pass

    root = None
    if hasattr(kernel, 'desktop') and kernel.desktop and hasattr(kernel.desktop, 'root'):
        root = kernel.desktop.root
    if root:
        root.after(0, _do_close)
    else:
        kernel.commands.execute(kernel, "close_app", app_name)

    return f"Closed {app_name}."


def list_apps(kernel) -> str:

    state = kernel.commands.execute(kernel, "list_apps")

    installed = ", ".join(state["installed"]) or "none"
    running = ", ".join(state["running"]) or "none"

    return f"Installed: {installed}. Running: {running}."


SKILLS = (
    Skill(
        tool=Tool(
            name="open_app",
            description="Open a NovaOS application window.",
            parameters=string_parameters(
                app_name="Exact application name, e.g. Notes, Browser, Calculator."
            ),
        ),
        run=open_app,
    ),
    Skill(
        tool=Tool(
            name="close_app",
            description="Close a running NovaOS application.",
            parameters=string_parameters(
                app_name="Exact name of the running application to close."
            ),
        ),
        run=close_app,
    ),
    Skill(
        tool=Tool(
            name="list_apps",
            description="List which applications are installed and which are running.",
        ),
        run=list_apps,
    ),
)