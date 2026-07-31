import customtkinter as ctk


class NovaApp(ctk.CTkFrame):
    """
    Base class for every NovaOS application.
    """

    APP_NAME = "Application"
    APP_ICON = "📦"

    def __init__(self, window):
        self.window = window
        self.content = window.content

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