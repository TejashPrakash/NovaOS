import customtkinter as ctk
from apps.file_manager.services.icons import get_icon

class FileList(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.buttons = []

        self.selected = None

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
        """Show AI context menu for a file."""
        try:
            from ai.ui.ai_context_menu import AIContextMenu
            # Walk up to find a root window
            widget = self
            while hasattr(widget, 'master') and widget.master:
                widget = widget.master
                if isinstance(widget, (ctk.CTkToplevel, ctk.CTk)):
                    break
            AIContextMenu(widget, file_path=str(file_path))
        except Exception as e:
            print(f"[FileList] Context menu error: {e}")