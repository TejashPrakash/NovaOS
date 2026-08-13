"""Glassmorphism UI components for NovaOS."""

import customtkinter as ctk


class GlassFrame(ctk.CTkFrame):
    """Glassmorphism frame with blur effect simulation."""

    def __init__(self, master, blur_amount: int = 15, opacity: float = 0.8, **kwargs):
        super().__init__(master, **kwargs)
        self.blur_amount = blur_amount
        self.opacity = opacity

        # Simulate glass effect
        self.configure(
            fg_color="#161B22",
            border_width=1,
            border_color="#FFFFFF40"
        )


class GlassCard(GlassFrame):
    """Glass card component for content display."""

    def __init__(self, master, title: str = "", icon: str = "", **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.icon = icon
        self._setup_ui()

    def _setup_ui(self):
        """Setup glass card UI."""
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
                    text_color="#00E5FF"
                )
                icon_label.pack(side="left", padx=(0, 10))

            if self.title:
                title_label = ctk.CTkLabel(
                    header,
                    text=self.title,
                    font=("Segoe UI", 14, "bold"),
                    text_color="#00E5FF"
                )
                title_label.pack(side="left")

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.pack(fill="both", expand=True, padx=15, pady=(0, 10))


class GlassButton(ctk.CTkButton):
    """Glassmorphism button with hover effects."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#161B22",
            text_color="#00E5FF",
            hover_color="#00E5FF",
            hover_text_color="black",
            border_width=1,
            border_color="#FFFFFF40",
            **kwargs
        )