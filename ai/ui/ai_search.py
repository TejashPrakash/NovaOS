"""AI-powered desktop search for NovaOS — understands natural language queries."""

import os
from pathlib import Path

import customtkinter as ctk
from core.theme import ThemeManager
from apps.registry import APP_REGISTRY


class AISearchDialog(ctk.CTkToplevel):
    """Full-screen AI search that understands natural language queries."""

    def __init__(self, master, kernel=None, **kwargs):
        super().__init__(master, **kwargs)

        self.kernel = kernel
        self.theme = ThemeManager()

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#050810")

        screen_w = self.winfo_screenwidth()
        self.geometry(f"600x400+{(screen_w - 600) // 2}+120")

        self._build_ui()
        self.after(100, lambda: self.search_entry.focus())

        # Close on Escape
        self.bind("<Escape>", lambda e: self._close())
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _build_ui(self):
        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color="#0D1117", corner_radius=12)
        search_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            search_frame, text="◈",
            font=("Segoe UI Emoji", 20),
            text_color="#00E5FF"
        ).pack(side="left", padx=(14, 6), pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Ask Nova anything... (e.g. 'open browser', 'what time is it', 'create a note')",
            height=44,
            fg_color="transparent",
            text_color="#FFFFFF",
            placeholder_text_color="#555555",
            border_width=0,
            font=("Segoe UI", 15)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)
        self.search_entry.bind("<Return>", self._execute)
        self.search_entry.bind("<KeyRelease>", self._on_type)

        # Results area
        self.results_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self._show_welcome()

    def _show_welcome(self):
        self._clear_results()

        ctk.CTkLabel(
            self.results_frame,
            text="Try asking:",
            font=("Segoe UI", 12, "bold"),
            text_color="#888888"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        examples = [
            ("🤖", "What time is it?"),
            ("🤖", "Open the browser"),
            ("🤖", "What's the weather?"),
            ("🤖", "Create a new note"),
            ("🤖", "Show system status"),
            ("🤖", "List all apps"),
        ]

        for icon, example in examples:
            btn = ctk.CTkButton(
                self.results_frame,
                text=f"  {icon}  {example}",
                height=34, anchor="w",
                fg_color="#161B22",
                text_color="#BBBBBB",
                hover_color="#1C2333",
                corner_radius=8,
                font=("Segoe UI", 12),
                command=lambda e=example: self._run_example(e)
            )
            btn.pack(fill="x", padx=5, pady=2)

    def _run_example(self, example):
        self.search_entry.delete(0, "end")
        self.search_entry.insert(0, example)
        self._execute()

    def _on_type(self, event=None):
        """Live search as user types."""
        query = self.search_entry.get().strip().lower()
        if len(query) < 2:
            self._show_welcome()
            return

        self._clear_results()

        # Search apps
        app_matches = []
        for name in APP_REGISTRY:
            if query in name.lower():
                app_matches.append(name)

        if app_matches:
            ctk.CTkLabel(
                self.results_frame, text="📱 Apps",
                font=("Segoe UI", 12, "bold"),
                text_color="#00E5FF"
            ).pack(anchor="w", padx=10, pady=(8, 4))

            for name in app_matches[:5]:
                icon = APP_REGISTRY[name].APP_ICON if hasattr(APP_REGISTRY[name], 'APP_ICON') else "📦"
                btn = ctk.CTkButton(
                    self.results_frame,
                    text=f"  {icon}  {name}",
                    height=34, anchor="w",
                    fg_color="#161B22", text_color="#CCCCCC",
                    hover_color="#00E5FF", corner_radius=8,
                    font=("Segoe UI", 12),
                    command=lambda n=name: self._launch_app(n)
                )
                btn.pack(fill="x", padx=5, pady=2)

        # Search notes
        self._search_notes(query)

        # Search files
        self._search_files(query)

    def _search_notes(self, query):
        """Search notes for matching content."""
        try:
            from apps.notes.services.notes_repository import NotesRepository
            repo = NotesRepository()
            notes = repo.list_notes()
            matches = [n for n in notes if query in n.get("title", "").lower() or query in n.get("content", "").lower()]

            if matches:
                ctk.CTkLabel(
                    self.results_frame, text="📝 Notes",
                    font=("Segoe UI", 12, "bold"),
                    text_color="#FF9800"
                ).pack(anchor="w", padx=10, pady=(8, 4))

                for note in matches[:3]:
                    btn = ctk.CTkButton(
                        self.results_frame,
                        text=f"  📄  {note['title']}",
                        height=34, anchor="w",
                        fg_color="#161B22", text_color="#CCCCCC",
                        hover_color="#1C2333", corner_radius=8,
                        font=("Segoe UI", 12),
                        command=lambda n=note: self._open_note(n)
                    )
                    btn.pack(fill="x", padx=5, pady=2)
        except Exception:
            pass

    def _search_files(self, query):
        """Search common directories for matching files."""
        try:
            home = Path.home()
            matches = []
            search_dirs = [home / "Desktop", home / "Documents", home / "Downloads"]

            for d in search_dirs:
                if d.exists():
                    for f in d.iterdir():
                        if query in f.name.lower():
                            matches.append(f)
                            if len(matches) >= 5:
                                break
                if len(matches) >= 5:
                    break

            if matches:
                ctk.CTkLabel(
                    self.results_frame, text="📁 Files",
                    font=("Segoe UI", 12, "bold"),
                    text_color="#4CAF50"
                ).pack(anchor="w", padx=10, pady=(8, 4))

                for f in matches:
                    btn = ctk.CTkButton(
                        self.results_frame,
                        text=f"  📄  {f.name}",
                        height=34, anchor="w",
                        fg_color="#161B22", text_color="#CCCCCC",
                        hover_color="#1C2333", corner_radius=8,
                        font=("Segoe UI", 12),
                        command=lambda p=str(f): self._open_file(p)
                    )
                    btn.pack(fill="x", padx=5, pady=2)
        except Exception:
            pass

    def _execute(self):
        """Execute the search query as an AI command."""
        query = self.search_entry.get().strip()
        if not query:
            return

        self._clear_results()

        # Show thinking
        ctk.CTkLabel(
            self.results_frame, text="🤖 Thinking...",
            font=("Segoe UI", 13),
            text_color="#888888"
        ).pack(pady=20)

        def run():
            if self.kernel and hasattr(self.kernel, 'ai') and self.kernel.ai.assistant:
                try:
                    response = self.kernel.ai.assistant.ask(query)
                    self._clear_results()
                    ctk.CTkLabel(
                        self.results_frame, text=response,
                        font=("Segoe UI", 13),
                        text_color="#BBBBBB",
                        wraplength=520,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=10)
                except Exception as e:
                    self._clear_results()
                    ctk.CTkLabel(
                        self.results_frame, text=f"Error: {e}",
                        font=("Segoe UI", 13),
                        text_color="#E53935"
                    ).pack(pady=20)
            else:
                self._clear_results()
                ctk.CTkLabel(
                    self.results_frame,
                    text="AI not configured. Set GEMINI_API_KEY in .env",
                    font=("Segoe UI", 13),
                    text_color="#FFC107"
                ).pack(pady=20)

        self.after(100, run)

    def _launch_app(self, name):
        if self.kernel:
            self.kernel.process_manager.start_process(name)
        self._close()

    def _open_note(self, note):
        if self.kernel:
            self.kernel.process_manager.start_process("Notes")
        self._close()

    def _open_file(self, path):
        if self.kernel:
            self.kernel.process_manager.start_process("Viewer")
        self._close()

    def _clear_results(self):
        for w in self.results_frame.winfo_children():
            w.destroy()

    def _close(self):
        try:
            self.destroy()
        except Exception:
            pass
