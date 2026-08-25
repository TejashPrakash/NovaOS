import os
from pathlib import Path
from datetime import datetime

import customtkinter as ctk
from tkinter import filedialog, messagebox
from sdk.app import NovaApp
from core.theme import ThemeManager


class EditorApp(NovaApp):
    """NovaOS Text Editor with file operations and AI assist."""

    APP_NAME = "Editor"
    APP_ICON = "📝"
    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 650

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self.current_file = None
        self.is_modified = False

    def build(self):
        # Toolbar
        self._build_toolbar()

        # Editor area
        self.editor = ctk.CTkTextbox(
            self.content,
            fg_color="#0A0E14",
            text_color="#BBBBBB",
            font=("Cascadia Code", 14),
            wrap="word",
            corner_radius=8
        )
        self.editor.pack(fill="both", expand=True, padx=10, pady=(5, 0))
        self.editor.bind("<<Modified>>", self._on_modified)

        # Status bar
        self._build_status_bar()

        # New file
        self._update_title("Untitled")
        self.editor.focus()

    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(
            self.content, fg_color="#161B22", height=45, corner_radius=8
        )
        toolbar.pack(fill="x", padx=10, pady=(10, 5))
        toolbar.pack_propagate(False)

        buttons = [
            ("📄 New", self.new_file),
            ("📂 Open", self.open_file),
            ("💾 Save", self.save_file),
            ("📋 Save As", self.save_as),
            ("|", None),
            ("↩ Undo", self._undo),
            ("↪ Redo", self._redo),
        ]

        for text, cmd in buttons:
            if text == "|":
                sep = ctk.CTkFrame(toolbar, width=2, fg_color="#333333")
                sep.pack(side="left", padx=8, pady=8, fill="y")
                continue
            btn = ctk.CTkButton(
                toolbar, text=text, width=90, height=30,
                fg_color="#252B3B", hover_color="#3A4256",
                text_color="#BBBBBB", corner_radius=6,
                font=("Segoe UI", 12),
                command=cmd
            )
            btn.pack(side="left", padx=3, pady=7)

    def _build_status_bar(self):
        status_bar = ctk.CTkFrame(
            self.content, fg_color="#161B22", height=30, corner_radius=0
        )
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        self.file_label = ctk.CTkLabel(
            status_bar, text="Untitled",
            font=("Segoe UI", 11), text_color="#888888", anchor="w"
        )
        self.file_label.pack(side="left", padx=10)

        self.stats_label = ctk.CTkLabel(
            status_bar, text="Ln 1, Col 1  |  0 words",
            font=("Segoe UI", 11), text_color="#888888", anchor="e"
        )
        self.stats_label.pack(side="right", padx=10)

        self.after(500, self._update_stats)

    def _update_title(self, name):
        modified = " *" if self.is_modified else ""
        title = f"{name}{modified} — Editor"
        self.window.title_label.configure(text=title) if hasattr(self.window, 'title_label') else None
        self.file_label.configure(text=name + modified)

    def _update_stats(self):
        try:
            content = self.editor.get("1.0", "end-1c")
            lines = content.count("\n") + 1
            words = len(content.split())
            self.stats_label.configure(text=f"{lines} lines  |  {words} words")
        except Exception:
            pass
        self.after(500, self._update_stats)

    def _on_modified(self, event=None):
        if not self.is_modified:
            self.is_modified = True
            self._update_title(
                Path(self.current_file).name if self.current_file else "Untitled"
            )
        self.editor.edit_modified(False)

    # =====================================================
    # File Operations
    # =====================================================

    def new_file(self):
        self.editor.delete("1.0", "end")
        self.current_file = None
        self.is_modified = False
        self._update_title("Untitled")

    def open_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Text Files", "*.txt *.py *.js *.html *.css *.json *.md"),
                ("All Files", "*.*")
            ]
        )
        if path:
            try:
                content = Path(path).read_text(encoding="utf-8", errors="replace")
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", content)
                self.current_file = path
                self.is_modified = False
                self._update_title(Path(path).name)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.current_file:
            self._write_file(self.current_file)
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("Python", "*.py"),
                ("All Files", "*.*")
            ]
        )
        if path:
            self._write_file(path)
            self.current_file = path
            self._update_title(Path(path).name)

    def _write_file(self, path):
        try:
            content = self.editor.get("1.0", "end-1c")
            Path(path).write_text(content, encoding="utf-8")
            self.is_modified = False
            self._update_title(Path(path).name)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

    def _undo(self):
        try:
            self.editor.edit_undo()
        except Exception:
            pass

    def _redo(self):
        try:
            self.editor.edit_redo()
        except Exception:
            pass