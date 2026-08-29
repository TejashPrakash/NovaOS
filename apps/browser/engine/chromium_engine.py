"""NovaOS Browser Engine — Playwright headless Chromium.

Full JavaScript/CSS/HTML5 browser that renders INSIDE NovaOS.

How it works:
  1. Headless Chromium runs in a background thread via Playwright
  2. Pages are rendered to screenshots
  3. Screenshots are displayed in a tkinter Canvas inside NovaOS
  4. Mouse clicks are mapped to Chromium coordinates
  5. Keyboard input is forwarded to Chromium

This gives a REAL browser inside NovaOS with zero external dependencies.
"""

import io
import queue
import sys
import threading
import time
from urllib.parse import urlparse

from PIL import Image, ImageTk

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class ChromiumBrowserEngine:
    """Full Chromium browser inside NovaOS using Playwright.

    Renders pages to screenshots and displays them in a tkinter Canvas.
    Supports full JavaScript, CSS, images, videos, forms.
    """

    def __init__(self):
        self.current_url = None
        self.widget = None          # tkinter Canvas for display
        self._parent_frame = None
        self._embedded = False
        self._browser = None
        self._page = None
        self._pw = None
        self._thread = None
        self._cmd_queue = queue.Queue()
        self._screenshot_queue = queue.Queue()
        self._running = False
        self._photo = None          # prevent GC
        self._width = 1200
        self._height = 700
        self._resize_after_id = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_webview(self, parent, url="about:blank"):
        self._parent_frame = parent

        if self.widget is not None:
            # Resize existing viewport to match current parent size
            self._sync_viewport_size()
            return self.widget

        if not PLAYWRIGHT_AVAILABLE:
            print("[Browser] Playwright not installed")
            return None

        try:
            self._create_browser(parent, url)
            return self.widget
        except Exception as e:
            print(f"[Browser] Browser creation failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def start(self):
        pass

    def stop(self):
        """Cleanly shut down Playwright Chromium."""
        self._running = False
        self._cmd_queue.put(("stop", None))
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3)
        if self._page:
            try:
                self._page.close()
            except Exception:
                pass
            self._page = None
        if self._browser:
            try:
                self._browser.close()
            except Exception:
                pass
            self._browser = None
        if self._pw:
            try:
                self._pw.stop()
            except Exception:
                pass
            self._pw = None
        self._embedded = False

    def is_available(self):
        return PLAYWRIGHT_AVAILABLE

    # --- Navigation ---------------------------------------------------

    def load(self, url):
        self.current_url = url
        self._cmd_queue.put(("goto", url))

    def reload(self):
        self._cmd_queue.put(("reload", None))

    def back(self):
        self._cmd_queue.put(("back", None))

    def forward(self):
        self._cmd_queue.put(("forward", None))

    def get_current_url(self):
        return self.current_url or "about:blank"

    def get_page_text(self):
        if self._page:
            try:
                return self._page.evaluate("document.body ? document.body.innerText : ''") or ""
            except Exception:
                pass
        return ""

    def evaluate_js(self, script):
        if self._page:
            try:
                return self._page.evaluate(script)
            except Exception:
                pass
        return None

    def find_text(self, query):
        return False

    def save_page(self, path):
        return False

    # --- Mouse/Keyboard input (called from tkinter events) -----------

    def handle_click(self, x, y):
        """Forward a click to Chromium at canvas coordinates."""
        self._cmd_queue.put(("click", (x, y)))

    def handle_key(self, key):
        """Forward a keypress to Chromium."""
        self._cmd_queue.put(("key", key))

    def handle_type(self, text):
        """Forward typed text to Chromium."""
        self._cmd_queue.put(("type", text))

    def handle_scroll(self, delta_y):
        """Forward mouse wheel scroll to Chromium.

        delta_y > 0 = scroll up, delta_y < 0 = scroll down.
        """
        if delta_y > 0:
            self._cmd_queue.put(("scroll_up", None))
        else:
            self._cmd_queue.put(("scroll_down", None))

    # ------------------------------------------------------------------
    # Browser thread
    # ------------------------------------------------------------------

    def _sync_viewport_size(self):
        """Sync Chromium viewport size with the actual parent frame size."""
        if not self._parent_frame or not self._widget_ready():
            return
        try:
            self._parent_frame.update_idletasks()
            new_w = max(400, self._parent_frame.winfo_width())
            new_h = max(300, self._parent_frame.winfo_height())
            if new_w != self._width or new_h != self._height:
                self._width = new_w
                self._height = new_h
                self._cmd_queue.put(("resize", (new_w, new_h)))
        except Exception:
            pass

    def _widget_ready(self):
        return self.widget is not None

    def _create_browser(self, parent, url):
        """Create the Canvas and start the browser thread."""
        import tkinter as tk
        self.widget = tk.Canvas(
            parent, highlightthickness=0, bg="#0D1117"
        )
        self.widget.pack(fill="both", expand=True)

        # Bind mouse events
        self.widget.bind("<Button-1>", self._on_click)
        self.widget.bind("<Button-2>", lambda e: None)
        self.widget.bind("<Button-3>", lambda e: None)

        # Bind mouse wheel for scrolling
        self.widget.bind("<MouseWheel>", self._on_scroll)       # Windows/macOS
        self.widget.bind("<Button-4>", self._on_scroll_up)      # Linux scroll up
        self.widget.bind("<Button-5>", self._on_scroll_down)    # Linux scroll down

        # Bind keyboard for arrow keys, Page Up/Down, Home/End
        self.widget.bind("<Up>", lambda e: self.handle_key("ArrowUp"))
        self.widget.bind("<Down>", lambda e: self.handle_key("ArrowDown"))
        self.widget.bind("<Prior>", lambda e: self.handle_key("PageUp"))
        self.widget.bind("<Next>", lambda e: self.handle_key("PageDown"))
        self.widget.bind("<Home>", lambda e: self.handle_key("Home"))
        self.widget.bind("<End>", lambda e: self.handle_key("End"))
        self.widget.bind("<space>", lambda e: self.handle_key("PageDown"))

        # Make canvas focusable for keyboard events
        self.widget.configure(cursor="hand2")
        self.widget.focus_set()

        # Click to focus
        self.widget.bind("<Button-1>", self._on_click_focus)

        # Detect actual size from parent
        parent.update_idletasks()
        self._width = max(800, parent.winfo_width())
        self._height = max(600, parent.winfo_height())

        # Start browser thread
        self._running = True
        self._thread = threading.Thread(
            target=self._browser_worker, args=(url,), daemon=True
        )
        self._thread.start()

        # Start screenshot display loop
        self._display_loop()

        self._embedded = True
        print("[Browser] Playwright Chromium ready")

    def _on_click_focus(self, event):
        """Handle click: focus canvas and forward to Chromium."""
        if self.widget:
            self.widget.focus_set()
        self._on_click(event)

    def _on_scroll(self, event):
        """Handle mouse wheel on Windows/macOS."""
        # event.delta > 0 = scroll up, < 0 = scroll down
        self.handle_scroll(event.delta)

    def _on_scroll_up(self, event):
        """Handle scroll up on Linux."""
        self.handle_scroll(1)

    def _on_scroll_down(self, event):
        """Handle scroll down on Linux."""
        self.handle_scroll(-1)

    def _browser_worker(self, initial_url):
        """Run headless Chromium in background thread."""
        try:
            self._pw = sync_playwright().start()
            self._browser = self._pw.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu"]
            )
            self._page = self._browser.new_page(
                viewport={"width": self._width, "height": self._height}
            )

            # Navigate to initial URL
            if initial_url and initial_url != "about:home":
                self._page.goto(initial_url, wait_until="domcontentloaded", timeout=30000)
                self.current_url = self._page.url
                self._take_screenshot()

            # Process commands
            while self._running:
                try:
                    cmd, data = self._cmd_queue.get(timeout=0.1)
                except queue.Empty:
                    # Periodic screenshot to catch page changes
                    try:
                        if self._page and not self._page.is_closed():
                            self._take_screenshot()
                    except Exception:
                        pass
                    continue

                if cmd == "stop":
                    break
                elif cmd == "goto":
                    try:
                        self._page.goto(data, wait_until="domcontentloaded", timeout=30000)
                        self.current_url = self._page.url
                        self._take_screenshot()
                    except Exception as e:
                        print(f"[Browser] Navigate error: {e}")
                elif cmd == "reload":
                    try:
                        self._page.reload(wait_until="domcontentloaded")
                        self.current_url = self._page.url
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "back":
                    try:
                        self._page.go_back(wait_until="domcontentloaded")
                        self.current_url = self._page.url
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "forward":
                    try:
                        self._page.go_forward(wait_until="domcontentloaded")
                        self.current_url = self._page.url
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "click":
                    try:
                        x, y = data
                        self._page.mouse.click(x, y)
                        time.sleep(0.5)
                        self.current_url = self._page.url
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "key":
                    try:
                        self._page.keyboard.press(data)
                        time.sleep(0.2)
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "type":
                    try:
                        self._page.keyboard.type(data)
                        time.sleep(0.2)
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "scroll_down":
                    try:
                        self._page.mouse.wheel(0, 3)
                        time.sleep(0.15)
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "scroll_up":
                    try:
                        self._page.mouse.wheel(0, -3)
                        time.sleep(0.15)
                        self._take_screenshot()
                    except Exception:
                        pass
                elif cmd == "resize":
                    try:
                        w, h = data
                        self._page.set_viewport_size({"width": w, "height": h})
                        time.sleep(0.2)
                        self._take_screenshot()
                    except Exception:
                        pass

        except Exception as e:
            print(f"[Browser] Browser thread error: {e}")

    def _take_screenshot(self):
        """Capture current page as screenshot."""
        if not self._page or self._page.is_closed():
            return
        try:
            screenshot = self._page.screenshot(type="png")
            try:
                self._screenshot_queue.get_nowait()  # discard old
            except queue.Empty:
                pass
            self._screenshot_queue.put(screenshot)
        except Exception:
            pass

    def _display_loop(self):
        """Display screenshots in the tkinter Canvas."""
        if not self._running or not self.widget:
            return
        try:
            while not self._screenshot_queue.empty():
                screenshot = self._screenshot_queue.get_nowait()
                self._display_screenshot(screenshot)
        except queue.Empty:
            pass
        except Exception:
            pass

        # Schedule next update
        if self._running and self.widget:
            try:
                self.widget.after(100, self._display_loop)
            except Exception:
                pass

    def _display_screenshot(self, png_data):
        """Display a PNG screenshot on the Canvas."""
        try:
            img = Image.open(io.BytesIO(png_data))
            cw = self.widget.winfo_width()
            ch = self.widget.winfo_height()
            if cw < 10 or ch < 10:
                return

            # Scale to fit canvas while preserving aspect ratio
            scale = min(cw / img.width, ch / img.height, 1.0)
            new_w = int(img.width * scale)
            new_h = int(img.height * scale)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            self._photo = ImageTk.PhotoImage(img)
            self.widget.delete("all")
            # Center in canvas
            x = (cw - new_w) // 2
            y = (ch - new_h) // 2
            self.widget.create_image(x, y, anchor="nw", image=self._photo)
        except Exception:
            pass

    def _on_click(self, event):
        """Forward click to Chromium."""
        if not self._page or self._page.is_closed():
            return

        try:
            cw = self.widget.winfo_width()
            ch = self.widget.winfo_height()

            if self._photo:
                img_w = self._photo.width()
                img_h = self._photo.height()
            else:
                return

            # Offset from centering
            offset_x = (cw - img_w) // 2
            offset_y = (ch - img_h) // 2

            # Map to page coordinates
            page_x = event.x - offset_x
            page_y = event.y - offset_y

            # Scale to viewport size
            if img_w > 0 and img_h > 0:
                scale_x = self._width / img_w
                scale_y = self._height / img_h
                page_x = int(page_x * scale_x)
                page_y = int(page_y * scale_y)

                page_x = max(0, min(page_x, self._width))
                page_y = max(0, min(page_y, self._height))

                self.handle_click(page_x, page_y)
        except Exception:
            pass
