from sdk.app import NovaApp
from apps.browser.services.bookmarks import BookmarkService
from apps.browser.controller.browser_controller import BrowserController
from apps.browser.services.browser_engine import BrowserEngine
from apps.browser.ui.statusbar import BrowserStatusBar
from apps.browser.ui.toolbar import BrowserToolbar
from apps.browser.ui.homepage import BrowserHomepage
from apps.browser.ui.tabs import BrowserTabs


class BrowserApp(NovaApp):

    APP_NAME = "Browser"

    APP_ICON = "🌐"

    # =====================================================

    def __init__(self, window):

        super().__init__(window)

        self.controller = BrowserController()

        self.engine = BrowserEngine()

        self.bookmarks = BookmarkService()

        self.tabs = []

        self.current_tab = None

        self.next_tab_id = 1

    # =====================================================

    def create_new_tab(self):

        from apps.browser.models.tab import BrowserTab

        tab = BrowserTab(
            id=self.next_tab_id
        )

        self.next_tab_id += 1

        self.tabs.append(tab)

        self.current_tab = tab

        return tab

    # =====================================================

    def new_tab(self):

        self.create_new_tab()

        self.refresh_tabs()

    # =====================================================

    def switch_tab(self, tab):

        self.current_tab = tab

        self.refresh_tabs()

    # =====================================================

    def close_tab(self, tab):

        if len(self.tabs) == 1:
            return

        self.tabs.remove(tab)

        if self.current_tab == tab:
            self.current_tab = self.tabs[-1]

        self.refresh_tabs()

    # =====================================================

    def refresh_tabs(self):

        self.tabs_bar.refresh(
            self.tabs,
            self.current_tab
        )

    # =====================================================

    def update_current_tab(self, url, title):

        if self.current_tab is None:
            return

        self.current_tab.url = url
        self.current_tab.title = title

        self.refresh_tabs()

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

        self.tabs_bar = BrowserTabs(self.content)

        self.tabs_bar.pack(
            fill="x",
            padx=8,
            pady=(8, 0)
        )

        self.tabs_bar.set_callbacks(
            self.switch_tab,
            self.close_tab,
            self.new_tab
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

        self.create_new_tab()
        self.refresh_tabs()

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

        self.update_current_tab(url, bookmark["title"])

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

        self.update_current_tab(url, url)

        self.statusbar.set_status(
            f"Loaded {url}"
        )

        self.update_navigation()

    # =====================================================

    def back(self):

        url = self.controller.go_back()

        self.toolbar.set_url(url)

        self.engine.load(url)
        self.update_current_tab(url, url)
        self.update_navigation()

    # =====================================================

    def forward(self):

        url = self.controller.go_forward()

        self.toolbar.set_url(url)

        self.engine.load(url)

        self.update_current_tab(url, url)

        self.update_navigation()

    # =====================================================

    def home(self):

        url = self.controller.go_home()

        self.toolbar.set_url(url)

        self.statusbar.set_status("Loading Home...")

        self.engine.load(url)

        self.update_current_tab(url, "Home")

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

        self.update_current_tab(url, query)

        self.update_navigation()