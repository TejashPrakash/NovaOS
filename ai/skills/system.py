"""Skills that report on and control the NovaOS system itself."""

import psutil

from ai.providers import Tool
from ai.skills.base import Skill


def system_status(kernel) -> str:

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    processes = len(kernel.process_manager.get_processes())

    return (
        f"CPU {psutil.cpu_percent(interval=0.1):.0f}%, "
        f"RAM {memory.percent:.0f}% of {memory.total / 1_000_000_000:.1f} GB, "
        f"disk {disk.percent:.0f}% used, "
        f"{processes} NovaOS app(s) running."
    )


def shutdown(kernel) -> str:

    kernel.commands.execute(kernel, "shutdown")

    return "Shutting down NovaOS."


SKILLS = (
    Skill(
        tool=Tool(
            name="system_status",
            description="Report CPU, memory and disk usage plus running app count.",
        ),
        run=system_status,
    ),
    Skill(
        tool=Tool(
            name="shutdown",
            description="Shut down NovaOS. Only use when the user clearly asks to.",
        ),
        run=shutdown,
    ),
)