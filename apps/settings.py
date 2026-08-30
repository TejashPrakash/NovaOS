"""NovaOS Settings - fully functional settings application."""

import os
import platform
import customtkinter as ctk
from tkinter import filedialog

from sdk.app import NovaApp
from core.config import Config
from core.theme import ThemeManager


class SettingsApp(NovaApp):
    APP_NAME = "Settings"
    APP_ICON = "⚙"
    DEFAULT_WIDTH = 700
    DEFAULT_HEIGHT = 580

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self.config = Config.load()

    def build(self):
        self.scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=15, pady=10)
        ctk.CTkLabel(self.scroll, text="⚙  NovaOS Settings",
            font=("Segoe UI", 26, "bold"), text_color="#00E5FF"
        ).pack(anchor="w", pady=(0, 15))
        self._build_appearance_section()
        self._build_ai_section()
        self._build_wallpaper_section()
        self._build_system_section()
        self._build_about_section()

    def _build_appearance_section(self):
        frame = self._section("🎨  Appearance")
        row = self._option_row(frame)
        ctk.CTkLabel(row, text="Theme:", font=("Segoe UI", 12), text_color="#BBBBBB").pack(side="left")
        themes = ["cyberpunk", "midnight", "ocean", "forest", "sunset", "arctic", "neon"]
        self.theme_var = ctk.StringVar(value="cyberpunk")
        ctk.CTkComboBox(row, values=themes, variable=self.theme_var, width=160, height=32,
            fg_color="#161B22", text_color="#FFFFFF", button_color="#00E5FF",
            dropdown_fg_color="#161B22", corner_radius=8, command=self._on_theme_change
        ).pack(side="right")
        row2 = self._option_row(frame)
        ctk.CTkLabel(row2, text="Neural Background:", font=("Segoe UI", 12), text_color="#BBBBBB").pack(side="left")
        self.effects_switch = ctk.CTkSwitch(row2, text="", progress_color="#00E5FF",
            button_color="#FFFFFF", command=self._on_effects_toggle)
        self.effects_switch.pack(side="right")
        self.effects_switch.set(0)

    def _on_theme_change(self, choice):
        if hasattr(self.window, "kernel") and self.window.kernel:
            self.window.kernel.set_theme(choice.lower())

    def _on_effects_toggle(self):
        enabled = bool(self.effects_switch.get())
        desktop = getattr(getattr(self.window, "kernel", None), "desktop", None)
        if desktop:
            if enabled:
                desktop.enable_neural_network_background()
                desktop.enable_ambient_lighting()
            else:
                desktop.disable_neural_network_background()
                desktop.disable_ambient_lighting()

    def _build_ai_section(self):
        frame = self._section("🤖  AI Assistant")
        row = self._option_row(frame)
        ctk.CTkLabel(row, text="Provider:", font=("Segoe UI", 12), text_color="#BBBBBB").pack(side="left")
        from core.config import CONFIG
        self.provider_var = ctk.StringVar(value=CONFIG.provider)
        ctk.CTkComboBox(row, values=["gemini", "ollama", "none"], variable=self.provider_var,
            width=160, height=32, fg_color="#161B22", text_color="#FFFFFF",
            button_color="#00E5FF", dropdown_fg_color="#161B22", corner_radius=8
        ).pack(side="right")
        row2 = self._option_row(frame)
        ctk.CTkLabel(row2, text="API Key:", font=("Segoe UI", 12), text_color="#BBBBBB").pack(side="left")
        self.api_key_entry = ctk.CTkEntry(row2, width=250, height=32, fg_color="#161B22",
            text_color="#FFFFFF", corner_radius=8, placeholder_text="Enter key...")
        self.api_key_entry.pack(side="right")
        try:
            from core.config import CONFIG
            if hasattr(CONFIG, 'gemini_api_key') and CONFIG.gemini_api_key:
                self.api_key_entry.insert(0, CONFIG.gemini_api_key)
        except Exception:
            pass
        ctk.CTkButton(frame, text="💾  Save AI Settings", height=34, corner_radius=8,
            fg_color="#00E5FF", text_color="black", hover_color="#00C8E8",
            font=("Segoe UI", 12, "bold"), command=self._save_ai_settings
        ).pack(padx=15, pady=(5, 12))
        self.ai_status = ctk.CTkLabel(frame, text="", font=("Segoe UI", 10), text_color="#4CAF50")
        self.ai_status.pack(padx=15, pady=(0, 5))

    def _save_ai_settings(self):
        api_key = self.api_key_entry.get().strip()
        provider = self.provider_var.get()
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
        env_lines = []
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                env_lines = f.readlines()
        updated = False
        has_key = False
        has_provider = False
        for i, line in enumerate(env_lines):
            if line.startswith("GEMINI_API_KEY="):
                env_lines[i] = f"GEMINI_API_KEY={api_key}\n"
                has_key = True
            elif line.startswith("NOVA_PROVIDER="):
                env_lines[i] = f"NOVA_PROVIDER={provider}\n"
                has_provider = True
        if not has_key:
            env_lines.append(f"GEMINI_API_KEY={api_key}\n")
        if not has_provider:
            env_lines.append(f"NOVA_PROVIDER={provider}\n")
        with open(env_path, "w") as f:
            f.writelines(env_lines)
        self.ai_status.configure(text="✅ Saved! Restart to apply.", text_color="#4CAF50")

    def _build_wallpaper_section(self):
        frame = self._section("🖼  Wallpaper")
        row = self._option_row(frame)
        ctk.CTkLabel(row, text="Background:", font=("Segoe UI", 12), text_color="#BBBBBB").pack(side="left")
        ctk.CTkButton(row, text="📁 Choose Image", width=140, height=32,
            fg_color="#161B22", text_color="#00E5FF", hover_color="#1C2333",
            corner_radius=8, border_width=1, border_color="#333333",
            command=self._pick_wallpaper
        ).pack(side="right")
        ctk.CTkButton(row, text="🔄 AI Wallpaper", width=140, height=32,
            fg_color="#161B22", text_color="#7B61FF", hover_color="#1C2333",
            corner_radius=8, border_width=1, border_color="#333333",
            command=self._apply_ai_wallpaper
        ).pack(side="right", padx=(0, 8))
        self.wallpaper_status = ctk.CTkLabel(frame, text="", font=("Segoe UI", 10), text_color="#888888")
        self.wallpaper_status.pack(padx=15, pady=(0, 5))

    def _pick_wallpaper(self):
        path = filedialog.askopenfilename(title="Choose Wallpaper",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All", "*.*")])
        if path:
            try:
                desktop = getattr(getattr(self.window, "kernel", None), "desktop", None)
                if desktop:
                    desktop.set_background_image(path)
                    self.wallpaper_status.configure(
                        text=f"✅ Applied: {os.path.basename(path)}", text_color="#4CAF50")
            except Exception as e:
                self.wallpaper_status.configure(text=f"❌ {e}", text_color="#E53935")

    def _apply_ai_wallpaper(self):
        try:
            from core.ai_background import ensure_wallpaper
            path = ensure_wallpaper()
            desktop = getattr(getattr(self.window, "kernel", None), "desktop", None)
            if desktop:
                desktop.set_background_image(path)
                self.wallpaper_status.configure(text="✅ AI wallpaper applied!", text_color="#4CAF50")
        except Exception as e:
            self.wallpaper_status.configure(text=f"❌ {e}", text_color="#E53935")

    def _build_system_section(self):
        frame = self._section("💻  System Information")
        info = [
            ("OS", "NovaOS v0.1.0-alpha"),
            ("Platform", f"{platform.system()} {platform.release()}"),
            ("Python", platform.python_version()),
            ("Machine", platform.machine()),
            ("Processor", platform.processor() or "Unknown"),
            ("Node", platform.node()),
        ]
        for label, value in info:
            row = self._option_row(frame)
            ctk.CTkLabel(row, text=label + ":", font=("Segoe UI", 11), text_color="#888888").pack(side="left")
            ctk.CTkLabel(row, text=value, font=("Segoe UI", 11, "bold"), text_color="#FFFFFF").pack(side="right")

    def _build_about_section(self):
        frame = self._section("ℹ  About NovaOS")
        ctk.CTkLabel(frame,
            text="NovaOS - AI-Powered Desktop Operating System\nBuilt with CustomTkinter + Python\nPowered by Gemini / Ollama AI",
            font=("Segoe UI", 12), text_color="#888888", justify="center"
        ).pack(pady=10)
        ctk.CTkLabel(frame, text="Version 0.1.0-alpha  •  2026",
            font=("Segoe UI", 10), text_color="#555555"
        ).pack(pady=(0, 10))

    def _section(self, title):
        frame = ctk.CTkFrame(self.scroll, fg_color="#161B22",
            corner_radius=12, border_width=1, border_color="#222222")
        frame.pack(fill="x", pady=8)
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 15, "bold"),
            text_color="#00E5FF").pack(anchor="w", padx=15, pady=(12, 6))
        return frame

    def _option_row(self, parent):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=4)
        return row
