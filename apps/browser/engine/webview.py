try:
    from tkinterweb import HtmlFrame
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("[Browser] tkinterweb not available - webview disabled")

class BrowserWebView:
    def __init__(self, parent):
        if not WEBVIEW_AVAILABLE:
            self.frame = None
            print("[Browser] Running in placeholder mode - install tkinterweb for full functionality")
            return
        self.frame = HtmlFrame(parent)
        self.frame.load_website("https://www.google.com")
    
    def pack(self, **kwargs):
        if self.frame:
            self.frame.pack(**kwargs)
    
    def pack_forget(self):
        if self.frame:
            self.frame.pack_forget()
    
    def load(self, url):
        if not self.frame:
            print(f"[Browser] Would load: {url} (webview unavailable)")
            return
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.frame.load_website(url)
    
    def back(self):
        if self.frame:
            try:
                self.frame.back()
            except:
                pass
    
    def forward(self):
        if self.frame:
            try:
                self.frame.forward()
            except:
                pass
    
    def reload(self):
        if self.frame:
            try:
                self.frame.reload()
            except:
                pass