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
        self.content = getattr(window, "content", None)

        if self.content is None:
            raise AttributeError("Window must expose a content frame")

        super().__init__(
            self.content,
            fg_color="transparent",
            **kwargs
        )

        self.pack(fill="both", expand=True)

    # ======================================

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