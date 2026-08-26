"""About / System Info dialog for NovaOS."""

import time
import platform
import psutil
import customtkinter as ctk
from core.theme import ThemeManager


class AboutDialog(ctk.CTkToplevel):
    """Premium about dialog with system information and credits."""

    def __init__(self, master=None):
        super().__init__(master)

        self.theme = ThemeManager()
        self.title("About NovaOS")
        self.geometry("480x520")
        self.configure(fg_color="#0D1117")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._tick_uptime()

    def _build_ui(self):
        # Logo
        logo = ctk.CTkLabel(
            self, text="◈",
            font=("Segoe UI Emoji", 64),
            text_color="#00E5FF"
        )
        logo.pack(pady=(25, 5))

        # Title
        ctk.CTkLabel(
            self, text="NovaOS",
            font=("Segoe UI", 28, "bold"),
            text_color="#FFFFFF"
        ).pack()

        ctk.CTkLabel(
            self, text="v0.1.0-alpha",
            font=("Segoe UI", 13),
            text_color="#888888"
        ).pack(pady=(2, 15))

        # System info card
        info_frame = ctk.CTkFrame(
            self, fg_color="#161B22", corner_radius=12
        )
        info_frame.pack(fill="x", padx=30, pady=(0, 12))

        specs = [
            ("OS", f"NovaOS v0.1.0-alpha"),
            ("Platform", f"{platform.system()} {platform.release()}"),
            ("Architecture", platform.machine()),
            ("Python", platform.python_version()),
            ("CPU", f"{psutil.cpu_count(logical=True)} cores"),
            ("RAM", f"{psutil.virtual_memory().total // (1024**3)} GB"),
            ("Uptime", self._get_uptime()),
        ]

        self.uptime_label = None

        for label, value in specs:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)

            ctk.CTkLabel(
                row, text=label, font=("Segoe UI", 12),
                text_color="#888888", width=100, anchor="w"
            ).pack(side="left")

            lbl = ctk.CTkLabel(
                row, text=value, font=("Segoe UI", 12, "bold"),
                text_color="#BBBBBB", anchor="w"
            )
            lbl.pack(side="left", fill="x", expand=True)

            if label == "Uptime":
                self.uptime_label = lbl

        # Separator
        ctk.CTkFrame(self, height=1, fg_color="#333333").pack(
            fill="x", padx=30, pady=(0, 12)
        )

        # Credits
        ctk.CTkLabel(
            self, text="Built with ❤️ using",
            font=("Segoe UI", 12),
            text_color="#888888"
        ).pack()

        tech_frame = ctk.CTkFrame(self, fg_color="transparent")
        tech_frame.pack(pady=(4, 10))

        techs = ["Python", "CustomTkinter", "psutil", "Gemini AI", "Ollama"]
        for tech in techs:
            ctk.CTkLabel(
                tech_frame, text=tech,
                font=("Segoe UI", 11, "bold"),
                text_color="#00E5FF"
            ).pack(side="left", padx=6)

        # Copyright
        ctk.CTkLabel(
            self, text="© 2026 NovaOS Project",
            font=("Segoe UI", 11),
            text_color="#555555"
        ).pack(pady=(0, 5))

        # Close button
        ctk.CTkButton(
            self, text="Close", width=120, height=36,
            fg_color="#161B22", text_color="#FFFFFF",
            hover_color="#1C2333", corner_radius=8,
            border_width=1, border_color="#333333",
            font=("Segoe UI", 13),
            command=self.destroy
        ).pack(pady=(0, 20))

    def _get_uptime(self):
        uptime_s = time.time() - psutil.boot_time()
        days = int(uptime_s // 86400)
        hours = int((uptime_s % 86400) // 3600)
        mins = int((uptime_s % 3600) // 60)
        if days:
            return f"{days}d {hours}h {mins}m"
        return f"{hours}h {mins}m"

    def _tick_uptime(self):
        if self.uptime_label:
            try:
                self.uptime_label.configure(text=self._get_uptime())
                self.after(60000, self._tick_uptime)
            except Exception:
                pass
