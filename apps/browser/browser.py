from core.base_app import BaseApp

from apps.browser.ui.toolbar import BrowserToolbar
from apps.browser.ui.homepage import BrowserHome


class BrowserApp(BaseApp):

    APP_NAME = "Browser"
    APP_ICON = "🌐"

    def __init__(self, window):

        super().__init__(window)

    def build(self):

        toolbar = BrowserToolbar(self.content)

        toolbar.pack(
            fill="x",
            padx=8,
            pady=(8, 0)
        )

        homepage = BrowserHome(self.content)

        homepage.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )