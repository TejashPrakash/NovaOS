import customtkinter as ctk


class NovaApp(ctk.CTkFrame):
    """
    Shared base class for NovaOS applications.
    """

    APP_NAME = "Application"
    APP_ICON = "📦"

    DEFAULT_WIDTH = 900
    DEFAULT_HEIGHT = 600

    def __init__(self, window, **kwargs):

        self.window = window
        window_content = getattr(window, "content", None)

        if window_content is None:
            raise AttributeError("Window must expose a content frame")

        super().__init__(
            window_content,
            fg_color="transparent",
            **kwargs
        )

        # NovaApp fills the window's available content area.
        self.pack(
            fill="both",
            expand=True
        )

        # Every app builds its widgets inside this frame.
        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True
        )

    # ======================================

    def create_container(self, parent=None):

        if parent is None:
            parent = self.content

        return ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

    def build(self):
        pass

    def on_open(self):
        pass

    def on_close(self):
        pass

    def on_focus(self):
        pass

    def on_blur(self):
        pass

    def refresh(self):
        pass

    def build_placeholder(self, title="Coming Soon"):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.pack(expand=True, fill="both")

        icon = ctk.CTkLabel(
            frame,
            text="🚧",
            font=("Segoe UI Emoji", 56)
        )
        icon.pack(pady=(80, 20))

        label = ctk.CTkLabel(
            frame,
            text=f"{title}\nComing Soon",
            font=("Segoe UI", 22, "bold"),
            justify="center"
        )
        label.pack()