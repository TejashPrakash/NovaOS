class BrowserEngine:
    """
    Browser engine abstraction.

    Today:
        - Stores the current URL.

    Future:
        - pywebview
        - QtWebEngine
        - CEF
    """

    def __init__(self):

        self.current_url = None

    # =====================================================

    def load(self, url):

        self.current_url = url

        print(f"[Browser] Loading: {url}")

    # =====================================================

    def reload(self):

        if self.current_url:

            print(f"[Browser] Reload: {self.current_url}")

    # =====================================================

    def get_current_url(self):

        return self.current_url