from apps.notes.services.notes_repository import NotesRepository


class NotesController:

    def __init__(self):

        self.repository = NotesRepository()

    # =========================================

    def get_notes(self):

        return self.repository.list_notes()

    # =========================================

    def get_note(self, note_id):

        return self.repository.get_note(note_id)

    # =========================================

    def create_note(self):

        return self.repository.create_note()

    # =========================================

    def update_note(
        self,
        note_id,
        title,
        content
    ):

        if not title.strip():
            title = "Untitled Note"

        return self.repository.update_note(
            note_id,
            title,
            content
        )

    # =========================================

    def delete_note(self, note_id):

        self.repository.delete_note(note_id)