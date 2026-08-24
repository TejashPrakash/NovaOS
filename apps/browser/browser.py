import customtkinter as ctk
from sdk.app import NovaApp
from apps.browser.controller import BrowserController
from apps.browser.services import BookmarkService, AIBrowserService
from apps.browser.ui import BrowserToolbar, BrowserTabs, BrowserHomepage, BrowserStatusBar
from apps.browser.models import BrowserTab
from apps.browser.engine import ChromiumBrowserEngine


class BrowserApp(NovaApp):
    APP_NAME = "Browser"
    APP_ICON = "🌐"
    DEFAULT_WIDTH = 1200
    DEFAULT_HEIGHT = 800

    def __init__(self, window):
        super().__init__(window)
        self.controller = BrowserController()
        self.bookmarks = BookmarkService()
        self.tabs = []
        self.current_tab = None
        self.next_tab_id = 1
        self.chromium_engine = None
        self.ai_service = None
        self.webview_widget = None

        # Initialize AI service
        try:
            if hasattr(window, 'kernel') and hasattr(window.kernel, 'ai'):
                self.ai_service = AIBrowserService(window.kernel.ai.assistant)
                print("[Browser] AI Service initialized")
        except:
            print("[Browser] AI Service not available")

    def create_new_tab(self):
        tab = BrowserTab(id=self.next_tab_id)
        self.next_tab_id += 1
        self.tabs.append(tab)
        self.current_tab = tab
        return tab

    def new_tab(self):
        self.create_new_tab()
        self.refresh_tabs()

    def switch_tab(self, tab):
        self.current_tab = tab
        self.toolbar.set_url("" if tab.url == "about:home" else tab.url)
        if tab.url == "about:home":
            self.homepage.pack(fill="both", expand=True, padx=8, pady=8)
        else:
            self.show_browser()
        self.statusbar.set_status(f"Tab: {tab.title}")
        self.refresh_tabs()
        self.update_navigation()

    def close_tab(self, tab):
        if len(self.tabs) == 1:
            return
        self.tabs.remove(tab)
        if self.current_tab == tab:
            self.current_tab = self.tabs[-1]
        self.refresh_tabs()
        self.update_navigation()

    def refresh_tabs(self):
        self.tabs_bar.refresh(self.tabs, self.current_tab)

    def update_current_tab(self, url, title):
        if self.current_tab is None:
            return
        self.current_tab.url = url
        self.current_tab.title = title
        self.refresh_tabs()

    def update_navigation(self):
        if not hasattr(self, "toolbar"):
            return
        tab = self.current_tab
        self.toolbar.back_btn.configure(
            state="normal" if tab is not None and self.controller.can_go_back(tab) else "disabled"
        )
        self.toolbar.forward_btn.configure(
            state="normal" if tab is not None and self.controller.can_go_forward(tab) else "disabled"
        )

    def ai_assist(self):
        """AI-powered browsing assistance."""
        if self.ai_service:
            dialog = ctk.CTkInputDialog(
                text="Ask Nova about this page (or type 'summary'):",
                title="Nova Browser AI",
            )
            question = dialog.get_input()
            if not question:
                return
            page_text = self.chromium_engine.get_page_text() if self.chromium_engine else ""
            if question.strip().lower() in {"summary", "summarize", "summarise"}:
                answer = self.ai_service.summarize_page(page_text)
            else:
                answer = self.ai_service.ask(question, page_text)
            self.statusbar.set_status(f"AI: {answer[:180]}")
        else:
            self.statusbar.set_status("AI unavailable. Configure a provider in Settings.")

    def show_browser(self):
        """Switch from homepage to browser view."""
        self.homepage.pack_forget()

        if not self.chromium_engine:
            self.statusbar.set_status("Browser engine unavailable")
            return

        url = self.current_tab.url if self.current_tab and self.current_tab.url else "https://www.google.com"
        self.chromium_engine.create_webview(self.content, url)
        self.chromium_engine.start()
        self.chromium_engine.load(url)

    def build(self):
        # Toolbar
        self.toolbar = BrowserToolbar(self.content)
        self.toolbar.pack(fill="x", padx=8, pady=(8, 0))

        # Tabs
        self.tabs_bar = BrowserTabs(self.content)
        self.tabs_bar.pack(fill="x", padx=8, pady=(8, 0))
        self.tabs_bar.set_callbacks(self.switch_tab, self.close_tab, self.new_tab)

        # Homepage
        self.homepage = BrowserHomepage(self.content)
        self.homepage.pack(fill="both", expand=True, padx=8, pady=8)
        self.homepage.load_bookmarks(self.bookmarks.get_all(), self.open_bookmark)

        # Statusbar
        self.statusbar = BrowserStatusBar(self.content)
        self.statusbar.pack(fill="x", padx=8, pady=(0, 8))

        # AI Button
        if self.ai_service:
            ai_btn = ctk.CTkButton(
                self.toolbar,
                text="✨ AI Assist",
                width=100,
                command=self.ai_assist
            )
            ai_btn.pack(side="right", padx=5)

        # Initialize Chromium engine
        try:
            self.chromium_engine = ChromiumBrowserEngine()
            print("[Browser] Chromium engine ready")
        except Exception as e:
            print(f"[Browser] Error initializing chromium: {e}")
            self.chromium_engine = None

        # Initial setup
        self.create_new_tab()
        self.toolbar.set_url(self.controller.go_home(self.current_tab))

        # Button actions
        self.toolbar.go_btn.configure(command=self.go)
        self.toolbar.back_btn.configure(command=self.back)
        self.toolbar.forward_btn.configure(command=self.forward)
        self.toolbar.home_btn.configure(command=self.home)
        self.toolbar.refresh_btn.configure(command=self.refresh)
        self.toolbar.bookmark_btn.configure(command=self.bookmark_current_page)
        self.toolbar.url_entry.bind("<Return>", lambda e: self.go())
        self.homepage.search_btn.configure(command=self.search)
        self.homepage.search.bind("<Return>", lambda e: self.search())

        self.update_navigation()
        self.refresh_tabs()

    def open_bookmark(self, bookmark):
        url = self.controller.navigate(self.current_tab, bookmark["url"])
        self.toolbar.set_url(url)
        self.statusbar.set_status(f"Opening {bookmark['title']}...")
        self.show_browser()
        self.update_current_tab(url, bookmark["title"])
        self.statusbar.set_status(f"Opened {bookmark['title']}")
        self.update_navigation()

    def go(self):
        url = self.toolbar.get_url()
        url = self.controller.navigate(self.current_tab, url)
        self.toolbar.set_url(url)
        self.statusbar.set_status("Loading...")
        self.show_browser()
        self.update_current_tab(url, url)
        self.statusbar.set_status(f"Loaded {url}")
        self.update_navigation()

    def back(self):
        url = self.controller.go_back(self.current_tab)
        self.toolbar.set_url(url)
        if self.chromium_engine:
            self.chromium_engine.back()
        self.update_current_tab(url, url)
        self.update_navigation()

    def forward(self):
        url = self.controller.go_forward(self.current_tab)
        self.toolbar.set_url(url)
        if self.chromium_engine:
            self.chromium_engine.forward()
        self.update_current_tab(url, url)
        self.update_navigation()

    def home(self):
        if self.chromium_engine and self.chromium_engine.widget:
            self.chromium_engine.widget.pack_forget()
        self.homepage.pack(fill="both", expand=True)
        self.toolbar.set_url("")
        self.statusbar.set_status("Home")
        self.update_current_tab("about:home", "Home")
        self.update_navigation()

    def refresh(self):
        self.statusbar.set_status("Refreshing...")
        if self.chromium_engine:
            self.chromium_engine.reload()
        self.statusbar.set_status("Ready")

    def bookmark_current_page(self):
        if not self.current_tab or not self.current_tab.url.startswith(("http://", "https://")):
            self.statusbar.set_status("Navigate to a page before bookmarking")
            return
        self.bookmarks.add(self.current_tab.title, self.current_tab.url)
        self.homepage.load_bookmarks(self.bookmarks.get_all(), self.open_bookmark)
        self.statusbar.set_status("Bookmark saved")

    def search(self):
        query = self.homepage.search.get()
        if not query:
            return
        url = self.controller.navigate(self.current_tab, query)
        self.toolbar.set_url(url)
        self.show_browser()
        self.update_current_tab(url, query)
        self.update_navigation()