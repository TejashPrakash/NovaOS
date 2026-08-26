import customtkinter as ctk
from sdk.app import NovaApp
from core.config import Config
from core.theme import ThemeManager


class SettingsApp(NovaApp):
    APP_NAME = "Settings"
    APP_ICON = "⚙"
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 500
    
    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self.config = Config.load()
    
    def build(self):
        """Build premium functional settings application."""
        main_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_label = ctk.CTkLabel(
            main_frame,
            text="⚙ NovaOS Settings",
            font=("Segoe UI", 28, "bold"),
            text_color=self.theme.get_color("primary")
        )
        header_label.pack(pady=(0, 20))
        
        self._setup_ai_settings(main_frame)
        self._setup_appearance_settings(main_frame)
        self._setup_system_settings(main_frame)
    
    def _create_section(self, parent, title):
        frame = ctk.CTkFrame(
            parent,
            fg_color=self.theme.get_color("surface_light"),
            corner_radius=12,
            border_width=1,
            border_color=self.theme.get_color("primary")
        )
        frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme.get_color("primary")
        ).pack(padx=15, pady=10)
        
        return frame
    
    def _setup_ai_settings(self, parent):
        ai_frame = self._create_section(parent, "🤖 AI Settings")
        
        ctk.CTkLabel(
            ai_frame,
            text="AI Provider:",
            font=("Segoe UI", 12),
            text_color=self.theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))
        
        provider_combo = ctk.CTkComboBox(
            ai_frame,
            values=["Gemini", "Ollama"],
            width=200,
            fg_color=self.theme.get_color("surface"),
            text_color=self.theme.get_color("text_primary"),
            dropdown_fg_color=self.theme.get_color("surface_light"),
            button_color=self.theme.get_color("primary")
        )
        provider_combo.set(self.config.provider.title())
        provider_combo.pack(padx=15, pady=(0, 10))
    
    def _setup_appearance_settings(self, parent):
        appearance_frame = self._create_section(parent, "🎨 Appearance")
        
        ctk.CTkLabel(
            appearance_frame,
            text="Premium Theme:",
            font=("Segoe UI", 12),
            text_color=self.theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))
        
        theme_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["Cyberpunk", "Neon", "Sunset", "Ocean"],
            width=200,
            fg_color=self.theme.get_color("surface"),
            text_color=self.theme.get_color("text_primary"),
            dropdown_fg_color=self.theme.get_color("surface_light"),
            button_color=self.theme.get_color("primary")
        )
        theme_combo.set(self.config.theme.title())
        theme_combo.pack(padx=15, pady=(0, 10))
        
        def apply_theme():
            theme_name = theme_combo.get().lower()
            if hasattr(self.window, "kernel") and hasattr(self.window.kernel, "desktop"):
                self.window.kernel.set_theme(theme_name)
            print(f"[Settings] Theme changed to {theme_name}")
        
        theme_combo.bind("<<ComboboxSelected>>", lambda _event: apply_theme())
        
        ctk.CTkLabel(
            appearance_frame,
            text="Premium Effects:",
            font=("Segoe UI", 12),
            text_color=self.theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))
        
        effects_switch = ctk.CTkSwitch(
            appearance_frame,
            text="Neural Background & Ambient Lighting",
            progress_color=self.theme.get_color("primary"),
            button_color=self.theme.get_color("primary"),
            onvalue=True,
            offvalue=False
        )
        effects_switch.set(self.config.glassmorphism_enabled)
        effects_switch.pack(padx=15, pady=(0, 10))
        
        def toggle_effects():
            enabled = bool(effects_switch.get())
            desktop = getattr(getattr(self.window, "kernel", None), "desktop", None)
            if desktop:
                if enabled:
                    desktop.enable_neural_network_background()
                    desktop.enable_ambient_lighting()
                else:
                    desktop.disable_neural_network_background()
                    desktop.disable_ambient_lighting()
            print(f"[Settings] Premium effects {'enabled' if enabled else 'disabled'}")
        
        effects_switch.configure(command=toggle_effects)
    
    def _setup_system_settings(self, parent):
        system_frame = self._create_section(parent, "💻 System")
        
        ctk.CTkLabel(
            system_frame,
            text="Window Animations:",
            font=("Segoe UI", 12),
            text_color=self.theme.get_color("text_primary")
        ).pack(padx=15, pady=(5, 2))
        
        animations_switch = ctk.CTkSwitch(
            system_frame,
            text="Enabled",
            progress_color=self.theme.get_color("primary"),
            button_color=self.theme.get_color("primary"),
            onvalue=True,
            offvalue=False
        )
        animations_switch.set(self.config.animations_enabled)
        animations_switch.pack(padx=15, pady=(0, 10))
        
        def toggle_animations():
            print(f"[Settings] Window animations {'enabled' if animations_switch.get() else 'disabled'}")
        
        animations_switch.configure(command=toggle_animations)