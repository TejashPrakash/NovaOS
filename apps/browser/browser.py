import customtkinter as ctk

from apps.browser.toolbar import BrowserToolbar
from apps.browser.home import BrowserHome


class BrowserApp:

    @staticmethod
    def build(window):

        # ===================================
        # Toolbar
        # ===================================

        toolbar = BrowserToolbar(window.content)

        toolbar.pack(
            fill="x",
            padx=8,
            pady=(8, 0)
        )

        # ===================================
        # Home Page
        # ===================================

        home = BrowserHome(window.content)

        home.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )