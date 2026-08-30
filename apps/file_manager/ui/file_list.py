import customtkinter as ctk
from apps.file_manager.services.icons import get_icon


class FileList(ctk.CTkScrollableFrame):

    def __init__(self, parent, fs=None):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.buttons = []
        self.selected = None
        self.fs = fs
        self._context_menu = None
        self._selected_path = None

    # ======================================================

    def clear(self):

        for button in self.buttons:
            button.destroy()

        self.buttons.clear()

        self.selected = None

    # ======================================================

    def load_items(self, items, open_callback):

        self.clear()

        for item in items:

            icon = get_icon(item)

            button = ctk.CTkButton(
                self,
                text=f"{icon}   {item.name}",
                anchor="w",
                height=38,
                fg_color="#252B3B",
                hover_color="#323A4D"
            )

            button.pack(
                fill="x",
                padx=4,
                pady=2
            )

            button.bind(
                "<Button-1>",
                lambda e, b=button: self.select(b)
            )

            button.bind(
                "<Double-Button-1>",
                lambda e, p=item: open_callback(p)
            )

            # Right-click AI context menu
            button.bind(
                "<Button-3>",
                lambda e, p=item: self._show_ai_context(p)
            )

            self.buttons.append(button)

    # ======================================================

    def select(self, button):

        if self.selected:

            self.selected.configure(
                fg_color="#252B3B"
            )

        button.configure(
            fg_color="#0078D7"
        )

        self.selected = button

    def _show_ai_context(self, file_path):
        """Show file operations context menu for a file."""
        self._selected_path = file_path
        # Destroy old menu if exists
        self._close_context()
        # Build context menu
        root = self.winfo_toplevel()
        self._context_menu = ctk.CTkToplevel(root)
        self._context_menu.overrideredirect(True)
        self._context_menu.attributes("-topmost", True)
        self._context_menu.configure(fg_color="#161B22")
        self._context_menu.geometry("+0+0")
        # Position at mouse
        x = root.winfo_pointerx()
        y = root.winfo_pointery()
        self._context_menu.geometry(f"180x{5*40+10}+{x}+{y}")

        items = []
        items.append(("📂 Open", lambda: self._ctx_open(file_path)))
        items.append(("📋 Copy", lambda: self._ctx_copy(file_path)))
        items.append(("✂️ Cut", lambda: self._ctx_cut(file_path)))
        items.append(("🗑️ Delete", lambda: self._ctx_delete(file_path)))
        items.append(("✏️ Rename", lambda: self._ctx_rename(file_path)))

        for text, cmd in items:
            btn = ctk.CTkButton(
                self._context_menu,
                text=text, anchor="w", height=36,
                fg_color="transparent", text_color="#CCCCCC",
                hover_color="#252B3B", corner_radius=0,
                font=("Segoe UI", 12),
                command=lambda c=cmd: (self._close_context(), c())
            )
            btn.pack(fill="x", padx=2, pady=1)

        # Close on click outside
        root.bind("<Button-1>", self._on_root_click, add="+")

    def _close_context(self):
        if self._context_menu:
            try:
                self._context_menu.destroy()
            except Exception:
                pass
            self._context_menu = None

    def _on_root_click(self, e):
        self._close_context()

    def _ctx_open(self, path):
        if path.is_dir() and self.fs:
            self.fs.open_folder(path)
            # Callback to refresh will be handled by the parent
            self.event_generate("<<RefreshNeeded>>")

    def _ctx_copy(self, path):
        if self.fs:
            self.fs.copy_file(path)

    def _ctx_cut(self, path):
        if self.fs:
            self.fs.cut_file(path)

    def _ctx_delete(self, path):
        if self.fs:
            self.fs.delete_file(path)
            self.event_generate("<<RefreshNeeded>>")

    def _ctx_rename(self, path):
        """Show inline rename dialog."""
        root = self.winfo_toplevel()
        dialog = ctk.CTkToplevel(root)
        dialog.title("Rename")
        dialog.geometry("350x150")
        dialog.configure(fg_color="#0D1117")
        dialog.attributes("-topmost", True)
        dialog.transient(root)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text="Rename to:",
            font=("Segoe UI", 13, "bold"), text_color="#FFFFFF"
        ).pack(pady=(15, 5))

        entry = ctk.CTkEntry(
            dialog, width=280, height=36,
            fg_color="#161B22", text_color="#FFFFFF",
            corner_radius=8
        )
        entry.pack(pady=5)
        entry.insert(0, path.name)
        entry.select_range(0, len(path.stem))
        entry.focus()

        def do_rename():
            new_name = entry.get().strip()
            if new_name and new_name != path.name:
                self.fs.rename_file(path, new_name)
                self.event_generate("<<RefreshNeeded>>")
            dialog.destroy()

        entry.bind("<Return>", lambda e: do_rename())

        ctk.CTkButton(
            dialog, text="Rename", height=32,
            fg_color="#00E5FF", text_color="black",
            hover_color="#00C8E8", corner_radius=8,
            command=do_rename
        ).pack(pady=10)