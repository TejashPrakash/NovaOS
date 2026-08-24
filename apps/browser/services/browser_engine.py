class BrowserEngine:
    """Browser engine placeholder - replaced by chromium_engine.py"""
    def __init__(self):
        self.current_url = None

    def load(self, url):
        self.current_url = url
        print(f"[BrowserEngine] Use chromium_engine instead")