"""Skills that read and write NovaOS notes."""

from apps.notes.services.notes_repository import NotesRepository

from ai.providers import Tool
from ai.skills.base import Skill, SkillError

_repository = None


def repository():
    """One repository for the whole AI layer, created on first use."""

    global _repository

    if _repository is None:
        _repository = NotesRepository()

    return _repository


def create_note(kernel, title: str = "", content: str = "") -> str:

    if not title.strip():
        raise SkillError("create_note needs a title")

    note = repository().create_note(title=title.strip(), content=content)

    if note is None:
        raise SkillError("the note could not be saved")

    return f"Created note {note['title']!r} (id {note['id']})."


def list_notes(kernel) -> str:

    notes = repository().list_notes()

    if not notes:
        return "There are no notes yet."

    titles = ", ".join(f"{note['title']} (id {note['id']})" for note in notes[:10])

    return f"{len(notes)} note(s). Most recent: {titles}."


SKILLS = (
    Skill(
        tool=Tool(
            name="create_note",
            description="Create a note in the NovaOS Notes app.",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Short note title."},
                    "content": {"type": "string", "description": "Body of the note."},
                },
                "required": ["title"],
            },
        ),
        run=create_note,
    ),
    Skill(
        tool=Tool(
            name="list_notes",
            description="List the notes stored in NovaOS, newest first.",
        ),
        run=list_notes,
    ),
)