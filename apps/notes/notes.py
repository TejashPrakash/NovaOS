from sdk.app import NovaApp

from apps.notes.controller.notes_controller import NotesController
from apps.notes.ui.sidebar import NotesSidebar
from apps.notes.ui.editor import NotesEditor
from apps.notes.ui.toolbar import NotesToolbar


class NotesApp(NovaApp):

    APP_NAME = "Notes"
    APP_ICON = "📝"

    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 650

    def __init__(self, window):

        super().__init__(window)

        self.controller = NotesController()

        self.selected_note = None

    # =====================================================

    def build(self):

        self.toolbar = NotesToolbar(self.content)
        self.toolbar.pack(fill="x")

        self.body = self.create_container(self.content)
        self.body.pack(fill="both", expand=True)

        self.sidebar = NotesSidebar(self.body)
        self.sidebar.pack(side="left", fill="y")

        self.editor = NotesEditor(self.body)
        self.editor.pack(side="left", fill="both", expand=True)

        # -------------------------
        # Toolbar Actions
        # -------------------------

        self.toolbar.new_button.configure(
            command=self.create_note
        )

        self.toolbar.delete_button.configure(
            command=self.delete_note
        )

        self.toolbar.save_button.configure(
            command=self.save_note
        )

        # -------------------------
        # Sidebar
        # -------------------------

        self.sidebar.set_callback(
            self.open_note
        )

        self.refresh_notes()

    # =====================================================

    def refresh_notes(self):

        notes = self.controller.get_notes()

        self.sidebar.load_notes(notes)

    # =====================================================

    def create_note(self):

        note = self.controller.create_note()

        self.refresh_notes()

        self.open_note(note["id"])

    # =====================================================

    def open_note(self, note_id):

        note = self.controller.get_note(note_id)

        if note is None:
            return

        self.selected_note = note

        self.editor.set_title(
            note["title"]
        )

        self.editor.set_content(
            note["content"]
        )

    # =====================================================

    def save_note(self):

        if self.selected_note is None:
            return

        title = self.editor.get_title()
        content = self.editor.get_content()

        self.selected_note = self.controller.update_note(
            self.selected_note["id"],
            title,
            content
        )

        self.refresh_notes()

    # =====================================================

    def delete_note(self):

        if self.selected_note is None:
            return

        self.controller.delete_note(
            self.selected_note["id"]
        )

        self.selected_note = None

        self.editor.clear()

        self.refresh_notes()