import customtkinter as ctk

from core.config import Config
from core.theme import ThemeManager


class SettingsApp:
    @staticmethod
    def build(window):
        """Build premium functional settings application."""
        theme = ThemeManager()
        config = Config.load()

        main_frame = ctk.CTkFrame(window.content, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_label = ctk.CTkLabel(
            main_frame,
            text="⚙ NovaOS Settings",
            font=("Segoe UI", 28, "bold"),
            text_color=theme.get_color("primary")
        )
        header_label.pack(pady=(0, 20))

        SettingsApp._setup_ai_settings(main_frame, theme, config)
        SettingsApp._setup_appearance_settings(main_frame, theme, config, window)
        SettingsApp._setup_system_settings(main_frame, theme, config)

    @staticmethod
    def _create_section(parent, theme, title):
        frame = ctk.CTkFrame(
            parent,
            fg_color=theme.get_color("surface_light"),
            corner_radius=12,
            border_width=1,
            border_color=theme.get_color("primary")
        )
        frame.pack(fill="x", pady=10)
        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color=theme.get_color("primary")
        ).pack(padx=15, pady=10)
        return frame

    @staticmethod
    def _setup_ai_settings(parent, theme, config):
        ai_frame = SettingsApp._create_section(parent, theme, "🤖 AI Settings")
        ctk.CTkLabel(
            ai_frame,
            text="AI Provider:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))

        provider_combo = ctk.CTkComboBox(
            ai_frame,
            values=["Gemini", "Ollama", "Claude"],
            width=200,
            fg_color=theme.get_color("surface"),
            text_color=theme.get_color("text_primary"),
            dropdown_fg_color=theme.get_color("surface_light"),
            button_color=theme.get_color("primary")
        )
        provider_combo.set(config.provider.title())
        provider_combo.pack(padx=15, pady=(0, 10))

    @staticmethod
    def _setup_appearance_settings(parent, theme, config, window):
        appearance_frame = SettingsApp._create_section(parent, theme, "🎨 Appearance")
        ctk.CTkLabel(
            appearance_frame,
            text="Premium Theme:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))

        theme_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["Cyberpunk", "Neon", "Sunset", "Ocean"],
            width=200,
            fg_color=theme.get_color("surface"),
            text_color=theme.get_color("text_primary"),
            dropdown_fg_color=theme.get_color("surface_light"),
            button_color=theme.get_color("primary")
        )
        theme_combo.set(config.theme.title())
        theme_combo.pack(padx=15, pady=(0, 10))

        def apply_theme():
            theme_name = theme_combo.get().lower()
            if hasattr(window, "kernel") and hasattr(window.kernel, "desktop"):
                window.kernel.set_theme(theme_name)
            print(f"[Settings] Theme changed to {theme_name}")

        theme_combo.bind("<<ComboboxSelected>>", lambda _event: apply_theme())

        ctk.CTkLabel(
            appearance_frame,
            text="Premium Effects:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))

        effects_switch = ctk.CTkSwitch(
            appearance_frame,
            text="Neural Background & Ambient Lighting",
            progress_color=theme.get_color("primary"),
            button_color=theme.get_color("primary"),
            onvalue=True,
            offvalue=False
        )
        effects_switch.set(config.glassmorphism_enabled)
        effects_switch.pack(padx=15, pady=(0, 10))

        def toggle_effects():
            enabled = bool(effects_switch.get())
            desktop = getattr(getattr(window, "kernel", None), "desktop", None)
            if desktop:
                if enabled:
                    desktop.enable_neural_background()
                    desktop.enable_ambient_lighting()
                else:
                    desktop.disable_neural_background()
                    desktop.disable_ambient_lighting()
            print(f"[Settings] Premium effects {'enabled' if enabled else 'disabled'}")

        effects_switch.configure(command=toggle_effects)

    @staticmethod
    def _setup_system_settings(parent, theme, config):
        system_frame = SettingsApp._create_section(parent, theme, "💻 System")
        ctk.CTkLabel(
            system_frame,
            text="Window Animations:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))

        animations_switch = ctk.CTkSwitch(
            system_frame,
            text="Enabled",
            progress_color=theme.get_color("primary"),
            button_color=theme.get_color("primary"),
            onvalue=True,
            offvalue=False
        )
        animations_switch.set(config.animations_enabled)
        animations_switch.pack(padx=15, pady=(0, 10))

        def toggle_animations():
            print(f"[Settings] Window animations {'enabled' if animations_switch.get() else 'disabled'}")

        animations_switch.configure(command=toggle_animations)