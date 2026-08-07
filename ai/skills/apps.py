"""Skills that drive NovaOS applications through the kernel command registry."""

from ai.providers import Tool
from ai.skills.base import Skill, SkillError, string_parameters


def open_app(kernel, app_name: str = "") -> str:

    if not app_name:
        raise SkillError("open_app needs an app_name")

    if not kernel.commands.execute(kernel, "open_app", app_name):
        raise SkillError(f"NovaOS has no application called {app_name!r}")

    return f"Opened {app_name}."


def close_app(kernel, app_name: str = "") -> str:

    if not app_name:
        raise SkillError("close_app needs an app_name")

    if not kernel.commands.execute(kernel, "close_app", app_name):
        return f"{app_name} was not running."

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