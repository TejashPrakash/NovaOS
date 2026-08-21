try:
    from apps.browser.engine.webview import BrowserWebView, WEBVIEW_AVAILABLE
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("[Browser] Webview module not available")

class BrowserEngine:
    """
    Browser engine abstraction.
    """
    def __init__(self):
        self.current_url = None
        self.webview = None
        self._webview_available = WEBVIEW_AVAILABLE
    
    def set_webview(self, webview):
        """Set the webview component for rendering."""
        self.webview = webview
    
    def load(self, url):
        self.current_url = url
        if self.webview and self._webview_available:
            self.webview.load(url)
        else:
            print(f"[Browser] Loading: {url} (placeholder mode)")
    
    def reload(self):
        if self.current_url:
            if self.webview and self._webview_available:
                self.webview.reload()
            else:
                print(f"[Browser] Reload: {self.current_url} (placeholder mode)")
    
    def get_current_url(self):
        return self.current_url
    
    def back(self):
        if self.webview and self._webview_available:
            self.webview.back()
        else:
            print("[Browser] Back (placeholder mode)")
    
    def forward(self):
        if self.webview and self._webview_available:
            self.webview.forward()
        else:
            print("[Browser] Forward (placeholder mode)")