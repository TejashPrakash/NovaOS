"""Glassmorphism UI components for NovaOS with theme integration."""
import customtkinter as ctk
from core.theme import ThemeManager


class GlassFrame(ctk.CTkFrame):
    """Glassmorphism frame with theme integration."""
    
    def __init__(self, master, blur_amount: int = 15, opacity: float = 0.8, **kwargs):
        super().__init__(master, **kwargs)
        self.blur_amount = blur_amount
        self.opacity = opacity
        self.theme = ThemeManager()
        
        self.configure(
            fg_color=self.theme.get_color("surface"),
            border_width=1,
            border_color=self.theme.get_color("primary")
        )


class GlassCard(GlassFrame):
    """Glass card component with theme integration."""
    
    def __init__(self, master, title: str = "", icon: str = "", **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.icon = icon
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup glass card UI with theme colors."""
        if self.title or self.icon:
            header = ctk.CTkFrame(
                self,
                fg_color="transparent"
            )
            header.pack(fill="x", padx=15, pady=10)
            
            if self.icon:
                icon_label = ctk.CTkLabel(
                    header,
                    text=self.icon,
                    font=("Segoe UI", 20),
                    text_color=self.theme.get_color("primary")
                )
                icon_label.pack(side="left", padx=(0, 10))
            
            if self.title:
                title_label = ctk.CTkLabel(
                    header,
                    text=self.title,
                    font=("Segoe UI", 14, "bold"),
                    text_color=self.theme.get_color("primary")
                )
                title_label.pack(side="left")
        
        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.pack(fill="both", expand=True, padx=15, pady=(0, 10))


class GlassButton(ctk.CTkButton):
    """Glassmorphism button with theme integration."""
    
    def __init__(self, master, **kwargs):
        self.theme = ThemeManager()
        
        # Set default colors from theme if not provided
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = self.theme.get_color("surface")
        if "text_color" not in kwargs:
            kwargs["text_color"] = self.theme.get_color("primary")
        if "hover_color" not in kwargs:
            kwargs["hover_color"] = self.theme.get_color("primary")
        if "border_color" not in kwargs:
            kwargs["border_color"] = self.theme.get_color("primary")
        
        super().__init__(
            master,
            border_width=1,
            **kwargs
        )