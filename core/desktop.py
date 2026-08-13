import customtkinter as ctk
from ai.ui.panel import AIPanel

class Desktop:

    def __init__(self, root):

        self.root = root

        # -----------------------------
        # Main Desktop Area
        # -----------------------------

        self.frame = ctk.CTkFrame(
            self.root,
            fg_color="#0D1117",
            corner_radius=0
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # -----------------------------
        # Wallpaper Layer
        # -----------------------------

        self.wallpaper = ctk.CTkLabel(
            self.frame,
            text="",
            fg_color="transparent"
        )

        self.wallpaper.place(
            relwidth=1,
            relheight=1
        )

        # -----------------------------
        # Desktop Widgets Layer
        # -----------------------------

        self.widget_layer = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.widget_layer.place(
            relwidth=1,
            relheight=1
        )

        # -----------------------------
        # Desktop Icons Layer
        # -----------------------------

        self.icon_layer = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.icon_layer.place(
            relwidth=1,
            relheight=1
        )

        self.ai_panel = None

    # ==========================================
    # Public API
    # ==========================================

    def get_canvas(self):

        return self.frame

    def get_widget_layer(self):

        return self.widget_layer

    def get_icon_layer(self):

        return self.icon_layer

    def toggle_ai_panel(self, assistant):
        """Toggle AI panel visibility."""
        if self.ai_panel is None:
            self.ai_panel = AIPanel(self.get_widget_layer(), assistant)
            self.ai_panel.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.ai_panel.destroy()
            self.ai_panel = None