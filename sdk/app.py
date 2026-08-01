import customtkinter as ctk


class NovaApp(ctk.CTkFrame):
    """
    Shared base class for NovaOS applications.
    """

    APP_NAME = "Application"
    APP_ICON = "📦"

    def __init__(self, window, **kwargs):
        self.window = window
        self.content = getattr(window, "content", None)

        if self.content is None:
            raise AttributeError("Window must expose a content frame")

        super().__init__(self.content, fg_color="transparent", **kwargs)
        self.pack(fill="both", expand=True)

    # ======================================

    def build(self):
        """
        Build the application's UI.
        """
        pass

    # ======================================

    def on_open(self):
        """
        Called when the app starts.
        """
        pass

    # ======================================

    def on_close(self):
        """
        Called before the app closes.
        """
        pass

    # ======================================

    def on_focus(self):
        """
        Called when the window gains focus.
        """
        pass

    # ======================================

    def on_blur(self):
        """
        Called when another window becomes active.
        """
        pass

    # ======================================

    def refresh(self):
        """
        Optional hook for subclasses that need to refresh UI state.
        """
        pass