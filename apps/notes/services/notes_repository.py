import sqlite3
from datetime import datetime
from pathlib import Path


class NotesRepository:
    """
    Stores NovaOS notes in the local SQLite database.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parents[3]

        self.database_path = (
            project_root / "database" / "nova.db"
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._create_table()

    def _connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def list_notes(self):
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, title, content, created_at, updated_at
                FROM notes
                ORDER BY updated_at DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def get_note(self, note_id):
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, title, content, created_at, updated_at
                FROM notes
                WHERE id = ?
                """,
                (note_id,)
            ).fetchone()

        return dict(row) if row else None

    def create_note(self, title="Untitled Note", content=""):
        now = datetime.now().isoformat(timespec="seconds")

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO notes (title, content, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (title, content, now, now)
            )

            note_id = cursor.lastrowid

        return self.get_note(note_id)

    def update_note(self, note_id, title, content):
        now = datetime.now().isoformat(timespec="seconds")

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE notes
                SET title = ?, content = ?, updated_at = ?
                WHERE id = ?
                """,
                (title, content, now, note_id)
            )

        return self.get_note(note_id)

    def delete_note(self, note_id):
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM notes WHERE id = ?",
                (note_id,)
            )