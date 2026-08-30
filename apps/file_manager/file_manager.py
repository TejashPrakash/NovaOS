from pathlib import Path

import customtkinter as ctk
from sdk.app import NovaApp

from apps.file_manager.services.filesystem import FileSystem
from apps.file_manager.ui.toolbar import FileToolbar
from apps.file_manager.ui.file_list import FileList


class FileManagerApp(NovaApp):

    APP_NAME = "Files"
    APP_ICON = "📁"
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600

    def __init__(self, window):
        super().__init__(window)
        self.fs = FileSystem()

    # ====================================================

    def build(self):
        # Toolbar
        self.toolbar = FileToolbar(self.content)
        self.toolbar.pack(fill="x", padx=8, pady=(8, 0))

        # File List (pass fs for file operations)
        self.file_list = FileList(self.content, fs=self.fs)
        self.file_list.pack(fill="both", expand=True, padx=8, pady=8)

        # Navigation button actions
        self.toolbar.refresh_btn.configure(command=self.refresh)
        self.toolbar.back_btn.configure(command=self.go_back)
        self.toolbar.forward_btn.configure(command=self.go_forward)
        self.toolbar.up_btn.configure(command=self.go_up)

        # File operation button actions
        self.toolbar.paste_btn.configure(command=self._paste)
        self.toolbar.new_folder_btn.configure(command=self._new_folder)

        # Listen for refresh events from context menu
        self.file_list.bind("<<RefreshNeeded>>", lambda e: self.refresh())

        # Initial Load
        self.refresh()

    # ====================================================

    def refresh(self):
        self.toolbar.set_path(self.fs.get_current_path())
        self.toolbar.back_btn.configure(
            state="normal" if self.fs.can_go_back() else "disabled"
        )
        self.toolbar.forward_btn.configure(
            state="normal" if self.fs.can_go_forward() else "disabled"
        )
        # Update paste button state
        if self.fs.has_clipboard():
            self.toolbar.paste_btn.configure(state="normal")
        else:
            self.toolbar.paste_btn.configure(state="disabled")
        self.file_list.load_items(self.fs.list_directory(), self.open_item)

    # ====================================================

    def go_up(self):
        self.fs.go_up()
        self.refresh()

    def go_back(self):
        self.fs.go_back()
        self.refresh()

    def go_forward(self):
        self.fs.go_forward()
        self.refresh()

    def open_item(self, item: Path):
        if item.is_dir():
            self.fs.open_folder(item)
            self.refresh()

    # ====================================================
    # File Operations
    # ====================================================

    def _paste(self):
        ok, msg = self.fs.paste_file()
        self.refresh()

    def _new_folder(self):
        """Show dialog to create a new folder."""
        root = self.content.winfo_toplevel()
        dialog = ctk.CTkToplevel(root)
        dialog.title("New Folder")
        dialog.geometry("350x150")
        dialog.configure(fg_color="#0D1117")
        dialog.attributes("-topmost", True)
        dialog.transient(root)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text="Folder name:",
            font=("Segoe UI", 13, "bold"), text_color="#FFFFFF"
        ).pack(pady=(15, 5))

        entry = ctk.CTkEntry(
            dialog, width=280, height=36,
            fg_color="#161B22", text_color="#FFFFFF",
            corner_radius=8, placeholder_text="New Folder"
        )
        entry.pack(pady=5)
        entry.focus()

        def do_create():
            name = entry.get().strip() or "New Folder"
            self.fs.create_folder(name)
            self.refresh()
            dialog.destroy()

        entry.bind("<Return>", lambda e: do_create())

        ctk.CTkButton(
            dialog, text="Create", height=32,
            fg_color="#00E5FF", text_color="black",
            hover_color="#00C8E8", corner_radius=8,
            command=do_create
        ).pack(pady=10)