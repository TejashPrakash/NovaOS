from pathlib import Path

from core.base_app import BaseApp

from apps.file_manager.services.filesystem import FileSystem
from apps.file_manager.ui.toolbar import FileToolbar
from apps.file_manager.ui.file_list import FileList


class FileManagerApp(BaseApp):

    APP_NAME = "Files"

    APP_ICON = "📁"

    def __init__(self, window):

        super().__init__(window)

        self.fs = FileSystem()

    # ====================================================

    def build(self):

        # Toolbar

        self.toolbar = FileToolbar(self.content)

        self.toolbar.pack(
            fill="x",
            padx=8,
            pady=(8, 0)
        )

        # File List

        self.file_list = FileList(self.content)

        self.file_list.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # Button Actions

        self.toolbar.refresh_btn.configure(
            command=self.refresh
        )

        self.toolbar.back_btn.configure(
            command=self.go_back
        )

        self.toolbar.forward_btn.configure(
            command=self.go_forward
        )

        self.toolbar.up_btn.configure(
            command=self.go_up
        )

        # Initial Load

        self.refresh()

    # ====================================================

    def refresh(self):

        self.toolbar.set_path(
            self.fs.get_current_path()
        )

        self.toolbar.back_btn.configure(
            state="normal" if self.fs.can_go_back() else "disabled"
        )

        self.toolbar.forward_btn.configure(
            state="normal" if self.fs.can_go_forward() else "disabled"
        )

        self.file_list.load_items(
            self.fs.list_directory(),
            self.open_item
        )

    # ====================================================

    def go_up(self):

        self.fs.go_up()

        self.refresh()

    def go_back(self):

        self.fs.go_back()

        self.refresh()

    # ====================================================

    def go_forward(self):

        self.fs.go_forward()

        self.refresh()

    # ====================================================

    def open_item(self, item: Path):

        if item.is_dir():

            self.fs.open_folder(item)

            self.refresh()