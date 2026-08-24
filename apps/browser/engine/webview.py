import webview
from typing import Optional, Callable


class WebviewEngine:
    """Browser engine using pywebview."""
    
    def __init__(self):
        self.window: Optional[webview.Window] = None
        self.current_url: str = ""
        self._loaded_callback: Optional[Callable] = None
    
    def create_window(self, title: str = "NovaOS Browser", 
                     url: str = "https://www.google.com",
                     width: int = 1024, height: int = 768) -> None:
        """Create a webview window."""
        self.window = webview.create_window(
            title=title,
            url=url,
            width=width,
            height=height,
            resizable=True
        )
        self.current_url = url
    
    def load_url(self, url: str) -> None:
        """Load a URL in the webview."""
        if self.window:
            self.window.load_url(url)
            self.current_url = url
        else:
            raise RuntimeError("Webview window not created")
    
    def go_back(self) -> None:
        """Go back in history."""
        if self.window:
            # Note: webview doesn't have built-in back/forward
            # This would need custom implementation
            pass
    
    def go_forward(self) -> None:
        """Go forward in history."""
        if self.window:
            # Note: webview doesn't have built-in back/forward
            # This would need custom implementation
            pass
    
    def reload(self) -> None:
        """Reload the current page."""
        if self.window:
            self.window.reload()
    
    def get_current_url(self) -> str:
        """Get the current URL."""
        return self.current_url
    
    def evaluate_js(self, script: str) -> None:
        """Evaluate JavaScript in the page."""
        if self.window:
            self.window.evaluate_js(script)
    
    def on_loaded(self, callback: Callable) -> None:
        """Set callback for page loaded event."""
        self._loaded_callback = callback
    
    def start(self) -> None:
        """Start the webview event loop."""
        if self.window:
            webview.start()
    
    def destroy(self) -> None:
        """Destroy the webview window."""
        if self.window:
            webview.destroy()
            self.window = None