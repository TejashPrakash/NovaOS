import customtkinter as ctk
from core.config import Config
from core.theme import ThemeManager


class SettingsApp:
    @staticmethod
    def build(window):
        """Build premium settings application with theme integration."""
        theme = ThemeManager()
        
        # Main container
        main_frame = ctk.CTkFrame(
            window.content,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_label = ctk.CTkLabel(
            main_frame,
            text="⚙ NovaOS Settings",
            font=("Segoe UI", 28, "bold"),
            text_color=theme.get_color("primary")
        )
        header_label.pack(pady=(0, 20))
        
        SettingsApp._setup_ai_settings(main_frame, theme)
        SettingsApp._setup_appearance_settings(main_frame, theme)
        SettingsApp._setup_system_settings(main_frame, theme)
    
    @staticmethod
    def _setup_ai_settings(parent, theme):
        """AI configuration settings with theme integration."""
        ai_frame = ctk.CTkFrame(
            parent,
            fg_color=theme.get_color("surface_light"),
            corner_radius=12,
            border_width=1,
            border_color=theme.get_color("primary_dim")
        )
        ai_frame.pack(fill="x", pady=10)
        
        label = ctk.CTkLabel(
            ai_frame,
            text="🤖 AI Settings",
            font=("Segoe UI", 16, "bold"),
            text_color=theme.get_color("primary")
        )
        label.pack(padx=15, pady=10)
        
        # Provider selection
        provider_label = ctk.CTkLabel(
            ai_frame,
            text="AI Provider:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        )
        provider_label.pack(padx=15, pady=(5, 2))
        
        provider_combo = ctk.CTkComboBox(
            ai_frame,
            values=["Gemini", "Ollama", "Claude"],
            width=200,
            fg_color=theme.get_color("surface"),
            text_color=theme.get_color("text_primary"),
            dropdown_fg_color=theme.get_color("surface_light"),
            button_color=theme.get_color("primary")
        )
        provider_combo.pack(padx=15, pady=(0, 10))
    
    @staticmethod
    def _setup_appearance_settings(parent, theme):
        """Appearance settings with premium theme options."""
        appearance_frame = ctk.CTkFrame(
            parent,
            fg_color=theme.get_color("surface_light"),
            corner_radius=12,
            border_width=1,
            border_color=theme.get_color("primary_dim")
        )
        appearance_frame.pack(fill="x", pady=10)
        
        label = ctk.CTkLabel(
            appearance_frame,
            text="🎨 Appearance",
            font=("Segoe UI", 16, "bold"),
            text_color=theme.get_color("primary")
        )
        label.pack(padx=15, pady=10)
        
        # Premium theme selection
        theme_label = ctk.CTkLabel(
            appearance_frame,
            text="Premium Theme:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        )
        theme_label.pack(padx=15, pady=(5, 2))
        
        theme_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["Cyberpunk", "Neon", "Sunset", "Ocean"],
            width=200,
            fg_color=theme.get_color("surface"),
            text_color=theme.get_color("text_primary"),
            dropdown_fg_color=theme.get_color("surface_light"),
            button_color=theme.get_color("primary")
        )
        theme_combo.pack(padx=15, pady=(0, 10))
        
        # Premium effects toggle
        effects_label = ctk.CTkLabel(
            appearance_frame,
            text="Premium Effects:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        )
        effects_label.pack(padx=15, pady=(5, 2))
        
        effects_switch = ctk.CTkSwitch(
            appearance_frame,
            text="Neural Background & Ambient Lighting",
            progress_color=theme.get_color("primary"),
            button_color=theme.get_color("primary")
        )
        effects_switch.pack(padx=15, pady=(0, 10))
    
    @staticmethod
    def _setup_system_settings(parent, theme):
        """System settings with theme integration."""
        system_frame = ctk.CTkFrame(
            parent,
            fg_color=theme.get_color("surface_light"),
            corner_radius=12,
            border_width=1,
            border_color=theme.get_color("primary_dim")
        )
        system_frame.pack(fill="x", pady=10)
        
        label = ctk.CTkLabel(
            system_frame,
            text="💻 System",
            font=("Segoe UI", 16, "bold"),
            text_color=theme.get_color("primary")
        )
        label.pack(padx=15, pady=10)
        
        # Window animations toggle
        animations_label = ctk.CTkLabel(
            system_frame,
            text="Window Animations:",
            font=("Segoe UI", 12),
            text_color=theme.get_color("text_primary")
        )
        animations_label.pack(padx=15, pady=(5, 2))
        
        animations_switch = ctk.CTkSwitch(
            system_frame,
            text="Enabled",
            progress_color=theme.get_color("primary"),
            button_color=theme.get_color("primary")
        )
        animations_switch.pack(padx=15, pady=(0, 10))