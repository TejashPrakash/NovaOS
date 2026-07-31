from core.base_app import BaseApp
from apps.browser.services.bookmarks import BookmarkService
from apps.browser.controller.browser_controller import BrowserController
from apps.browser.services.browser_engine import BrowserEngine
from apps.browser.ui.statusbar import BrowserStatusBar
from apps.browser.ui.toolbar import BrowserToolbar
from apps.browser.ui.homepage import BrowserHomepage


class BrowserApp(BaseApp):

    APP_NAME = "Browser"

    APP_ICON = "🌐"

    # =====================================================

    def __init__(self, window):

        super().__init__(window)

        self.controller = BrowserController()

        self.engine = BrowserEngine()

        self.bookmarks = BookmarkService()

    # =====================================================

    def update_navigation(self):

        self.toolbar.back_btn.configure(
            state="normal"
            if self.controller.can_go_back()
            else "disabled"
        )

        self.toolbar.forward_btn.configure(
            state="normal"
            if self.controller.can_go_forward()
            else "disabled"
        )

    # =====================================================

    def build(self):

        # ---------------------------------------
        # Toolbar
        # ---------------------------------------

        self.toolbar = BrowserToolbar(self.content)

        self.toolbar.pack(
            fill="x",
            padx=8,
            pady=(8, 0)
        )

        # ---------------------------------------
        # Homepage
        # ---------------------------------------

        self.homepage = BrowserHomepage(self.content)

        self.homepage.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.homepage.load_bookmarks(

            self.bookmarks.get_all(),

            self.open_bookmark
        )

        self.statusbar = BrowserStatusBar(self.content)

        self.statusbar.pack(
            fill="x",
            padx=8,
            pady=(0, 8)
        )

        # ---------------------------------------
        # Initial URL
        # ---------------------------------------

        self.toolbar.set_url(
            self.controller.get_home()
        )

        # ---------------------------------------
        # Button Actions
        # ---------------------------------------

        self.toolbar.go_btn.configure(
            command=self.go
        )

        self.toolbar.back_btn.configure(
            command=self.back
        )

        self.toolbar.forward_btn.configure(
            command=self.forward
        )

        self.toolbar.home_btn.configure(
            command=self.home
        )

        self.toolbar.refresh_btn.configure(
            command=self.refresh
        )

        self.toolbar.url_entry.bind(
            "<Return>",
            lambda e: self.go()
        )

        self.homepage.search_btn.configure(
            command=self.search
        )

        self.homepage.search.bind(
            "<Return>",
            lambda e: self.search()
        )

        self.update_navigation()

    # =====================================================

    def open_bookmark(self, bookmark):

        url = self.controller.navigate(
            bookmark["url"]
        )

        self.toolbar.set_url(url)

        self.statusbar.set_status(
            f"Opening {bookmark['title']}..."
        )

        self.engine.load(url)

        self.statusbar.set_status(
            f"Loaded {bookmark['title']}"
        )

        self.update_navigation()

    # =====================================================

    def go(self):

        url = self.toolbar.get_url()

        url = self.controller.navigate(url)

        self.toolbar.set_url(url)

        self.statusbar.set_status(
            "Loading..."
        )

        self.engine.load(url)

        self.statusbar.set_status(
            f"Loaded {url}"
        )

        self.update_navigation()

    # =====================================================

    def back(self):

        url = self.controller.go_back()

        self.toolbar.set_url(url)

        self.engine.load(url)

        self.update_navigation()

    # =====================================================

    def forward(self):

        url = self.controller.go_forward()

        self.toolbar.set_url(url)

        self.engine.load(url)

        self.update_navigation()

    # =====================================================

    def home(self):

        url = self.controller.go_home()

        self.toolbar.set_url(url)

        self.statusbar.set_status("Loading Home...")

        self.engine.load(url)

        self.statusbar.set_status("Home Loaded")

        self.update_navigation()

    # =====================================================

    def refresh(self):

        self.statusbar.set_status("Refreshing...")

        self.engine.reload()

        self.statusbar.set_status("Ready")

    # =====================================================

    def search(self):

        query = self.homepage.search.get()

        if not query:
            return

        url = self.controller.navigate(query)

        self.toolbar.set_url(url)

        self.engine.load(url)

        self.update_navigation()