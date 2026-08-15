import customtkinter as ctk
from core.config import Config


class SettingsApp:
    @staticmethod
    def build(window):
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
            text_color="#00E5FF"
        )
        header_label.pack(pady=(0, 20))
        
        SettingsApp._setup_ai_settings(main_frame)
        SettingsApp._setup_appearance_settings(main_frame)
        SettingsApp._setup_system_settings(main_frame)
        
    @staticmethod
    def _setup_ai_settings(parent):
        """AI configuration settings."""
        ai_frame = ctk.CTkFrame(
            parent,
            fg_color="#252B3B",
            corner_radius=12
        )
        ai_frame.pack(fill="x", pady=10)
        
        label = ctk.CTkLabel(
            ai_frame,
            text="🤖 AI Settings",
            font=("Segoe UI", 16, "bold"),
            text_color="#00E5FF"
        )
        label.pack(padx=15, pady=10)
        
        # Provider selection
        provider_label = ctk.CTkLabel(
            ai_frame,
            text="AI Provider:",
            font=("Segoe UI", 12)
        )
        provider_label.pack(padx=15, pady=(5, 2))
        
        provider_combo = ctk.CTkComboBox(
            ai_frame,
            values=["Gemini", "Ollama"],
            width=200
        )
        provider_combo.pack(padx=15, pady=(0, 10))
        
    @staticmethod
    def _setup_appearance_settings(parent):
        """Appearance settings."""
        appearance_frame = ctk.CTkFrame(
            parent,
            fg_color="#252B3B",
            corner_radius=12
        )
        appearance_frame.pack(fill="x", pady=10)
        
        label = ctk.CTkLabel(
            appearance_frame,
            text="🎨 Appearance",
            font=("Segoe UI", 16, "bold"),
            text_color="#00E5FF"
        )
        label.pack(padx=15, pady=10)
        
        # Theme selection
        theme_label = ctk.CTkLabel(
            appearance_frame,
            text="Theme:",
            font=("Segoe UI", 12)
        )
        theme_label.pack(padx=15, pady=(5, 2))
        
        theme_combo = ctk.CTkComboBox(
            appearance_frame,
            values=["Dark", "Light"],
            width=200
        )
        theme_combo.pack(padx=15, pady=(0, 10))
        
    @staticmethod
    def _setup_system_settings(parent):
        """System settings."""
        system_frame = ctk.CTkFrame(
            parent,
            fg_color="#252B3B",
            corner_radius=12
        )
        system_frame.pack(fill="x", pady=10)
        
        label = ctk.CTkLabel(
            system_frame,
            text="💻 System",
            font=("Segoe UI", 16, "bold"),
            text_color="#00E5FF"
        )
        label.pack(padx=15, pady=10)
        
        # Window animations toggle
        animations_label = ctk.CTkLabel(
            system_frame,
            text="Window Animations:",
            font=("Segoe UI", 12)
        )
        animations_label.pack(padx=15, pady=(5, 2))
        
        animations_switch = ctk.CTkSwitch(
            system_frame,
            text="Enabled",
            progress_color="#00E5FF"
        )
        animations_switch.pack(padx=15, pady=(0, 10))