"""File Viewer for NovaOS — displays images and text files."""

import os
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image, ImageTk
from sdk.app import NovaApp
from core.theme import ThemeManager

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".tiff"}
TEXT_EXTS = {
    ".txt", ".md", ".py", ".js", ".ts", ".html", ".css", ".json",
    ".xml", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".env",
    ".sh", ".bat", ".ps1", ".csv", ".log", ".sql", ".rs", ".go",
    ".java", ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".swift",
}


class ViewerApp(NovaApp):
    """File viewer for images and text files with zoom, pan, and info."""

    APP_NAME = "Viewer"
    APP_ICON = "👁"
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self._current_file = None
        self._image_original = None
        self._image_display = None
        self._zoom = 1.0
        self._pan_start = None

    def build(self):
        # Toolbar
        toolbar = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=8)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkButton(
            toolbar, text="📂 Open File", width=110, height=32,
            fg_color="#0D1117", text_color="#00E5FF",
            hover_color="#1C2333", corner_radius=8,
            border_width=1, border_color="#333333",
            font=("Segoe UI", 12),
            command=self._open_file
        ).pack(side="left", padx=8, pady=6)

        ctk.CTkButton(
            toolbar, text="📂 Open Image", width=110, height=32,
            fg_color="#0D1117", text_color="#00E5FF",
            hover_color="#1C2333", corner_radius=8,
            border_width=1, border_color="#333333",
            font=("Segoe UI", 12),
            command=self._open_image
        ).pack(side="left", padx=4, pady=6)

        self.file_label = ctk.CTkLabel(
            toolbar, text="No file loaded",
            font=("Segoe UI", 12), text_color="#888888"
        )
        self.file_label.pack(side="left", padx=10)

        # Zoom controls
        ctk.CTkButton(
            toolbar, text="🔍+", width=36, height=32,
            fg_color="#0D1117", text_color="#FFFFFF",
            hover_color="#1C2333", corner_radius=8,
            font=("Segoe UI", 13, "bold"),
            command=self._zoom_in
        ).pack(side="right", padx=(0, 4), pady=6)

        ctk.CTkButton(
            toolbar, text="🔍−", width=36, height=32,
            fg_color="#0D1117", text_color="#FFFFFF",
            hover_color="#1C2333", corner_radius=8,
            font=("Segoe UI", 13, "bold"),
            command=self._zoom_out
        ).pack(side="right", padx=4, pady=6)

        ctk.CTkButton(
            toolbar, text="Fit", width=40, height=32,
            fg_color="#0D1117", text_color="#FFFFFF",
            hover_color="#1C2333", corner_radius=8,
            font=("Segoe UI", 12),
            command=self._zoom_fit
        ).pack(side="right", padx=4, pady=6)

        # Content area — scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.content, fg_color="#0A0E14", corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Image display
        self.image_label = ctk.CTkLabel(
            self.scroll_frame, text="",
            fg_color="transparent"
        )

        # Text display
        self.text_display = ctk.CTkTextbox(
            self.scroll_frame,
            fg_color="#0A0E14",
            text_color="#BBBBBB",
            font=("Cascadia Code", 13),
            wrap="word",
            state="disabled",
            corner_radius=8
        )

        # Placeholder
        self._show_placeholder()

        # Info bar
        self.info_bar = ctk.CTkLabel(
            self.content, text="Ready",
            font=("Segoe UI", 11), text_color="#555555"
        )
        self.info_bar.pack(fill="x", padx=10)

    def _show_placeholder(self):
        self.image_label.pack_forget()
        self.text_display.pack_forget()

        self.placeholder = ctk.CTkLabel(
            self.scroll_frame,
            text="👁\n\nOpen a file to view it\n\nSupported: Images (PNG, JPG, GIF, BMP)\nText files (TXT, PY, JS, JSON, MD, etc.)",
            font=("Segoe UI", 16),
            text_color="#555555",
            justify="center"
        )
        self.placeholder.pack(expand=True, pady=80)

    def _open_file(self):
        all_exts = sorted(IMAGE_EXTS | TEXT_EXTS)
        ext_str = " ".join(f"*{e}" for e in all_exts)
        path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("All Supported", ext_str),
                ("Images", " ".join(f"*{e}" for e in IMAGE_EXTS)),
                ("Text Files", " ".join(f"*{e}" for e in TEXT_EXTS)),
                ("All Files", "*.*"),
            ]
        )
        if path:
            self._load_file(path)

    def _open_image(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Images", " ".join(f"*{e}" for e in IMAGE_EXTS)),
                ("All Files", "*.*"),
            ]
        )
        if path:
            self._load_file(path)

    def _load_file(self, path):
        ext = Path(path).suffix.lower()
        self._current_file = path
        name = Path(path).name
        size = os.path.getsize(path)

        self.file_label.configure(text=f"{name}  ({self._human_size(size)})")

        if ext in IMAGE_EXTS:
            self._load_image(path)
        elif ext in TEXT_EXTS:
            self._load_text(path)
        else:
            self._show_placeholder()
            self.info_bar.configure(text=f"Unsupported file type: {ext}")

    def _load_image(self, path):
        try:
            # Hide text, show image
            self.text_display.pack_forget()
            self.placeholder.destroy()

            img = Image.open(path)
            self._image_original = img.copy()
            self._zoom = 1.0
            self._display_image()

            self.info_bar.configure(
                text=f"{img.size[0]}×{img.size[1]} px | {Path(path).suffix.upper()[1:]}"
            )
        except Exception as e:
            self._show_placeholder()
            self.info_bar.configure(text=f"Error loading image: {e}")

    def _display_image(self):
        if self._image_original is None:
            return

        img = self._image_original
        w, h = img.size
        new_w = int(w * self._zoom)
        new_h = int(h * self._zoom)

        if new_w < 1 or new_h < 1:
            return

        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self._image_display = ImageTk.PhotoImage(resized)

        self.image_label.configure(image=self._image_display, text="")
        self.image_label.pack(expand=True, pady=10)

    def _load_text(self, path):
        try:
            # Hide image, show text
            self.image_label.pack_forget()
            self.placeholder.destroy()

            text = Path(path).read_text(encoding="utf-8", errors="replace")

            self.text_display.configure(state="normal")
            self.text_display.delete("1.0", "end")
            self.text_display.insert("1.0", text)
            self._apply_syntax_highlighting(Path(path).suffix.lower())
            self.text_display.configure(state="disabled")
            self.text_display.pack(fill="both", expand=True, padx=5, pady=5)

            lines = len(text.splitlines())
            chars = len(text)
            self.info_bar.configure(text=f"{lines} lines | {chars} characters")
        except Exception as e:
            self._show_placeholder()
            self.info_bar.configure(text=f"Error loading text: {e}")

    def _apply_syntax_highlighting(self, ext):
        """Apply syntax highlighting to the text display."""
        import re

        # Configure tags
        self.text_display.tag_config("keyword", foreground="#FF79C6")
        self.text_display.tag_config("string", foreground="#F1FA8C")
        self.text_display.tag_config("comment", foreground="#6272A4")
        self.text_display.tag_config("number", foreground="#BD93F9")
        self.text_display.tag_config("function", foreground="#50FA7B")

        # Language-specific patterns
        keywords = []
        if ext in {".py", ".pyw"}:
            keywords = ["import", "from", "def", "class", "return", "if", "elif", "else",
                       "for", "while", "try", "except", "finally", "with", "as", "in",
                       "not", "and", "or", "is", "None", "True", "False", "print",
                       "lambda", "yield", "raise", "pass", "break", "continue"]
        elif ext in {".js", ".ts", ".jsx", ".tsx"}:
            keywords = ["const", "let", "var", "function", "return", "if", "else",
                       "for", "while", "class", "import", "export", "default", "new",
                       "this", "true", "false", "null", "undefined", "async", "await",
                       "try", "catch", "finally", "throw", "switch", "case", "break"]
        elif ext in {".html", ".htm"}:
            keywords = ["html", "head", "body", "div", "span", "script", "style",
                       "link", "meta", "title", "table", "form", "input", "button"]
        elif ext in {".css", ".scss"}:
            keywords = ["color", "background", "margin", "padding", "border", "font",
                       "display", "position", "width", "height", "flex", "grid"]
        elif ext in {".json",}:
            keywords = ["true", "false", "null"]
        elif ext in {".rs",}:
            keywords = ["fn", "let", "mut", "pub", "struct", "enum", "impl", "use",
                       "mod", "if", "else", "match", "loop", "while", "for", "return",
                       "self", "Self", "true", "false", "Some", "None", "Ok", "Err"]
        elif ext in {".go",}:
            keywords = ["func", "package", "import", "var", "const", "type", "struct",
                       "interface", "if", "else", "for", "range", "return", "fmt",
                       "nil", "true", "false", "map", "chan", "go", "defer"]
        elif ext in {".java",}:
            keywords = ["public", "private", "protected", "class", "interface", "extends",
                       "implements", "new", "this", "super", "return", "if", "else",
                       "for", "while", "try", "catch", "finally", "void", "int", "String",
                       "true", "false", "null", "static", "final"]

        if not keywords:
            return  # No highlighting for this language

        try:
            content = self.text_display.get("1.0", "end")

            # Keywords
            for kw in keywords:
                for match in re.finditer(r'\b' + re.escape(kw) + r'\b', content):
                    start = f"1.0+{match.start()}c"
                    end = f"1.0+{match.end()}c"
                    self.text_display.tag_add("keyword", start, end)

            # Strings (single and double quoted)
            for match in re.finditer(r'("[^"\\]*(?:\\.[^"\\]*)*"|' + r"'[^'\\]*(?:\\.[^'\\]*)*')", content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_display.tag_add("string", start, end)

            # Comments (// and #)
            for match in re.finditer(r'(//.*$|#.*$)', content, re.MULTILINE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_display.tag_add("comment", start, end)

            # Numbers
            for match in re.finditer(r'\b\d+\.?\d*\b', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_display.tag_add("number", start, end)

            # Function calls
            for match in re.finditer(r'\b([a-zA-Z_]\w*)\s*(?=\()', content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_display.tag_add("function", start, end)
        except Exception:
            pass  # Silently skip highlighting errors

    # ------------------------------------------------------------------ zoom
    def _zoom_in(self):
        self._zoom = min(5.0, self._zoom * 1.25)
        self._display_image()

    def _zoom_out(self):
        self._zoom = max(0.1, self._zoom / 1.25)
        self._display_image()

    def _zoom_fit(self):
        if self._image_original is None:
            return
        # Fit to window
        try:
            win_w = self.scroll_frame.winfo_width() - 40
            win_h = self.scroll_frame.winfo_height() - 40
            img_w, img_h = self._image_original.size
            scale_x = win_w / img_w if img_w > 0 else 1
            scale_y = win_h / img_h if img_h > 0 else 1
            self._zoom = min(scale_x, scale_y, 1.0)
            self._display_image()
        except Exception:
            pass

    @staticmethod
    def _human_size(size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
