import customtkinter as ctk

from apps.browser.ui.toolbar import BrowserToolbar
from apps.browser.engine.webview import BrowserWebView


class BrowserApp:

    @staticmethod
    def build(window):

        browser = BrowserWebView(window.content)

        toolbar = BrowserToolbar(
            window.content,
            browser
        )

        toolbar.pack(
            fill="x",
            padx=8,
            pady=(8, 0)
        )

        browser.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )