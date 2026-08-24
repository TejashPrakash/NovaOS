import webbrowser
import subprocess
import sys
from urllib.parse import urlparse

try:
    from tkinterweb import HtmlFrame
except ImportError:
    HtmlFrame = None

try:
    import webview
except ImportError:
    webview = None

try:
    from PySide6 import QtWebEngineWidgets
    QT_WEBENGINE_AVAILABLE = True
except ImportError:
    QT_WEBENGINE_AVAILABLE = False

class ChromiumBrowserEngine:
    """Embedded browser engine with a TkinterWeb fallback path."""
    
    def __init__(self):
        self.current_url = None
        self.widget = None
        self.window = None
        self._using_embedded = False
        self._external_browser = False
        self._qt_process = None
        
    FULL_BROWSER_HOSTS = {
        "google.com", "www.google.com", "mail.google.com", "gmail.com",
        "accounts.google.com", "images.google.com", "news.google.com",
        "youtube.com", "www.youtube.com",
        "drive.google.com", "docs.google.com", "meet.google.com",
        "discord.com", "web.whatsapp.com", "netflix.com",
    }

    def requires_full_browser(self, url):
        host = urlparse(url).netloc.lower().split(":")[0]
        return host in self.FULL_BROWSER_HOSTS or any(
            host.endswith(f".{domain}") for domain in self.FULL_BROWSER_HOSTS
        )

    def create_webview(self, parent, url="about:blank"):
        """Create an embedded browser widget inside the NovaOS window."""
        if self.widget and self.requires_full_browser(url):
            self.widget.destroy()
            self.widget = None
        if self._qt_process and self._qt_process.poll() is None:
            self._qt_process.terminate()
            self._qt_process = None
        if self.widget or self.window:
            return self.widget or self.window

        if self.requires_full_browser(url):
            # pywebview's Windows backend must own the process main thread.
            # NovaOS already owns that thread with Tk, so launch the real
            # browser instead of starting a second GUI loop from a worker.
            self.current_url = url
            if QT_WEBENGINE_AVAILABLE:
                try:
                    self._qt_process = subprocess.Popen(
                        [sys.executable, "-m", "apps.browser.engine.qt_browser", url],
                        creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
                    )
                    self._external_browser = True
                    print(f"[Browser] Opened full Chromium window: {url}")
                    return None
                except OSError as error:
                    print(f"[Browser] Qt WebEngine unavailable: {error}")
            if webview is not None:
                self._external_browser = True
                webbrowser.open_new(url)
                return None
            print("[Browser] Full browser unavailable; using embedded renderer")

        try:
            if HtmlFrame is not None:
                self._external_browser = False
                self.widget = HtmlFrame(
                    parent,
                    messages_enabled=False,
                    javascript_enabled=True,
                    forms_enabled=True,
                    images_enabled=True,
                    threading_enabled=True,
                    width=1200,
                    height=700,
                )
                self.widget.pack(fill="both", expand=True, padx=8, pady=8)
                self._using_embedded = True
                return self.widget
        except Exception as error:
            print(f"[Browser] Embedded engine unavailable: {error}")

        if webview is None:
            return None
        try:
            self.window = webview.create_window("Nova Browser", "about:blank")
            return self.window
        except Exception as error:
            print(f"[Browser] Error creating fallback webview: {error}")
            return None

    def start(self):
        """Start the optional external fallback engine."""
        if self._using_embedded or not self.window or webview is None:
            return
        # pywebview is intentionally not started here. Its Windows GUI loop
        # cannot safely run alongside NovaOS's Tk main loop.
        return

    def is_available(self):
        return HtmlFrame is not None or QT_WEBENGINE_AVAILABLE or webview is not None

    def stop(self):
        if self.widget:
            self.widget.destroy()
        if self.window and webview is not None:
            try:
                self.window.destroy()
            except Exception:
                pass
        self.widget = None
        self.window = None
        self._using_embedded = False
        self._external_browser = False
        if self._qt_process and self._qt_process.poll() is None:
            self._qt_process.terminate()
        self._qt_process = None
    
    def load(self, url):
        self.current_url = url
        if self.widget:
            try:
                if url == "about:home":
                    self.widget.load_html("<h1>Nova Browser</h1><p>Ready for your next search.</p>")
                else:
                    self.widget.load_url(url)
                print(f"[Browser] Loading: {url}")
            except Exception as e:
                print(f"[Browser] Error loading URL: {e}")
        elif self.window:
            try:
                self.window.load_url(url)
            except Exception as error:
                print(f"[Browser] Unable to load page: {error}")
        elif self._external_browser:
            # Full Chromium was already launched by create_webview().
            return
    
    def reload(self):
        if self.widget:
            self.widget.reload()
        elif self.window:
            try:
                self.window.reload()
                print("[Browser] Reloaded")
            except:
                pass
    
    def back(self):
        if self.widget:
            self.widget.go_back()
        elif self.window:
            try:
                self.window.back()
            except:
                pass
    
    def forward(self):
        if self.widget:
            self.widget.go_forward()
        elif self.window:
            try:
                self.window.forward()
            except:
                pass
    
    def get_current_url(self):
        if self.widget:
            return self.widget.current_url or self.current_url
        return self.current_url

    def get_page_text(self):
        if self.widget:
            try:
                return self.widget.get_page_text() or ""
            except Exception:
                return ""
        if self.window:
            return self.evaluate_js("document.body ? document.body.innerText : ''") or ""
        return ""

    def find_text(self, query):
        if self.widget and query:
            return self.widget.find_text(query)
        return False

    def save_page(self, path):
        if self.widget:
            return self.widget.save_page(path)
        return False
    
    def evaluate_js(self, script):
        """Execute JavaScript in the browser."""
        if self.widget:
            try:
                return self.widget.execute_javascript(script)
            except Exception:
                return None
        if self.window:
            try:
                return self.window.evaluate_js(script)
            except:
                return None