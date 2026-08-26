"""AI-powered context menu for NovaOS — right-click to get AI actions on files and desktop."""

import os
from pathlib import Path

import customtkinter as ctk
from core.theme import ThemeManager


class AIContextMenu(ctk.CTkToplevel):
    """AI-enhanced right-click context menu with smart actions."""

    def __init__(self, master, kernel=None, file_path=None, **kwargs):
        super().__init__(master)

        self.kernel = kernel
        self.file_path = file_path
        self.theme = ThemeManager()

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0D1117")

        width = 260
        self.geometry(f"{width}x0+0+0")
        self.transient(master)

        self._build_menu()
        self._position_menu()

        # Close on click outside
        self.bind("<FocusOut>", lambda e: self._close())
        self.after(100, self.focus_set)

    def _build_menu(self):
        """Build the context menu items."""
        items = []

        if self.file_path:
            path = Path(self.file_path)
            ext = path.suffix.lower()

            # File info header
            self._add_header(f"{path.name}")

            if ext in {".txt", ".md", ".py", ".js", ".ts", ".json", ".html", ".css"}:
                items.append(("🤖", "AI: Summarize this file", self._ai_summarize))
                items.append(("🤖", "AI: Explain this code", self._ai_explain))
                items.append(("🤖", "AI: Find bugs", self._ai_find_bugs))

            if ext in {".txt", ".md"}:
                items.append(("🤖", "AI: Improve writing", self._ai_improve_writing))

            if ext in {".py", ".js", ".ts", ".java", ".c", ".cpp", ".rs", ".go"}:
                items.append(("🤖", "AI: Add comments", self._ai_add_comments))
                items.append(("🤖", "AI: Write tests", self._ai_write_tests))

            items.append(("separator", "", None))
            items.append(("📋", "Copy path", self._copy_path))
            items.append(("📂", "Open in Terminal", self._open_in_terminal))

            if ext in {".png", ".jpg", ".jpeg", ".gif", ".bmp"}:
                items.append(("👁", "Open in Viewer", self._open_in_viewer))

            items.append(("separator", "", None))
            items.append(("🗑", "Delete", self._delete_file))
        else:
            # Desktop context menu
            items.append(("🤖", "Ask Nova AI", self._ask_nova))
            items.append(("separator", "", None))
            items.append(("📝", "New Note", lambda: self._open_app("Notes")))
            items.append(("📅", "New Event", lambda: self._open_app("Calendar")))
            items.append(("separator", "", None))
            items.append(("📊", "System Monitor", lambda: self._open_app("System Monitor")))
            items.append(("⚙️", "Settings", lambda: self._open_app("Settings")))
            items.append(("separator", "", None))
            items.append(("🔒", "Lock Screen", self._lock_screen))

        for icon, label, callback in items:
            if icon == "separator":
                sep = ctk.CTkFrame(self, height=1, fg_color="#333333")
                sep.pack(fill="x", padx=10, pady=4)
            else:
                self._add_item(icon, label, callback)

    def _add_header(self, text):
        label = ctk.CTkLabel(
            self, text=text,
            font=("Segoe UI", 11, "bold"),
            text_color="#00E5FF",
            anchor="w"
        )
        label.pack(fill="x", padx=12, pady=(8, 4))

    def _add_item(self, icon, text, callback):
        btn = ctk.CTkButton(
            self, text=f"  {icon}  {text}",
            height=32, anchor="w",
            fg_color="transparent",
            text_color="#CCCCCC",
            hover_color="#1C2333",
            corner_radius=6,
            font=("Segoe UI", 12),
            command=lambda: self._run_and_close(callback)
        )
        btn.pack(fill="x", padx=6, pady=1)

    def _run_and_close(self, callback):
        try:
            callback()
        except Exception as e:
            print(f"[ContextMenu] Error: {e}")
        self._close()

    def _position_menu(self):
        """Position near the cursor."""
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = self.winfo_pointerx()
        y = self.winfo_pointery()

        # Keep on screen
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        if x + w > screen_w:
            x = screen_w - w - 5
        if y + h > screen_h:
            y = screen_h - h - 5

        self.geometry(f"+{x}+{y}")

    def _close(self):
        try:
            self.destroy()
        except Exception:
            pass

    # ------------------------------------------------------------------ AI actions
    def _ai_summarize(self):
        self._run_ai_action(
            f"Summarize the contents of this file in 3-5 bullet points: {self.file_path}"
        )

    def _ai_explain(self):
        self._run_ai_action(
            f"Explain what this code does, line by line if short, or section by section: {self.file_path}"
        )

    def _ai_find_bugs(self):
        self._run_ai_action(
            f"Review this code for bugs, errors, and potential issues: {self.file_path}"
        )

    def _ai_improve_writing(self):
        self._run_ai_action(
            f"Suggest improvements for this writing: {self.file_path}"
        )

    def _ai_add_comments(self):
        self._run_ai_action(
            f"Add inline comments to this code explaining what each section does: {self.file_path}"
        )

    def _ai_write_tests(self):
        self._run_ai_action(
            f"Write unit tests for this code: {self.file_path}"
        )

    def _run_ai_action(self, prompt):
        """Run an AI action and show the result in a dialog."""
        if not self.kernel or not hasattr(self.kernel, 'ai'):
            self._show_result("AI not configured. Set GEMINI_API_KEY in .env")
            return

        assistant = self.kernel.ai.assistant
        if not assistant:
            self._show_result("AI assistant not available")
            return

        # Read file content
        try:
            content = Path(self.file_path).read_text(encoding="utf-8", errors="replace")
            full_prompt = f"{prompt}\n\nFile content:\n```\n{content[:3000]}\n```"
        except Exception:
            full_prompt = prompt

        # Show thinking dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("AI Analysis")
        dialog.geometry("500x400")
        dialog.configure(fg_color="#0D1117")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text="🤖 AI Analysis",
            font=("Segoe UI", 16, "bold"),
            text_color="#00E5FF"
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            dialog, text="Analyzing...",
            font=("Segoe UI", 12),
            text_color="#888888"
        ).pack(pady=(0, 10))

        result_box = ctk.CTkTextbox(
            dialog, fg_color="#0A0E14", text_color="#BBBBBB",
            font=("Cascadia Code", 12), wrap="word",
            state="disabled"
        )
        result_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        def run():
            try:
                response = assistant.ask(full_prompt)
                result_box.configure(state="normal")
                result_box.insert("1.0", response)
                result_box.configure(state="disabled")
            except Exception as e:
                result_box.configure(state="normal")
                result_box.insert("1.0", f"Error: {e}")
                result_box.configure(state="disabled")

        dialog.after(100, run)

        ctk.CTkButton(
            dialog, text="Close", width=100, height=32,
            fg_color="#161B22", text_color="#FFFFFF",
            hover_color="#1C2333", corner_radius=8,
            command=dialog.destroy
        ).pack(pady=(0, 10))

    def _show_result(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Result")
        dialog.geometry("400x200")
        dialog.configure(fg_color="#0D1117")
        dialog.transient(self.winfo_toplevel())

        ctk.CTkLabel(
            dialog, text=message,
            font=("Segoe UI", 13), text_color="#BBBBBB",
            wraplength=350
        ).pack(expand=True, padx=20)

        ctk.CTkButton(
            dialog, text="OK", width=80,
            fg_color="#00E5FF", text_color="#000000",
            command=dialog.destroy
        ).pack(pady=(0, 15))

    # ------------------------------------------------------------------ utility actions
    def _copy_path(self):
        self.clipboard_clear()
        self.clipboard_append(str(self.file_path))

    def _open_in_terminal(self):
        if self.kernel:
            self.kernel.process_manager.start_process("Terminal")

    def _open_in_viewer(self):
        if self.kernel:
            self.kernel.process_manager.start_process("Viewer")

    def _delete_file(self):
        try:
            path = Path(self.file_path)
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
        except Exception as e:
            print(f"[ContextMenu] Delete failed: {e}")

    def _ask_nova(self):
        if self.kernel and hasattr(self.kernel, 'ai') and self.kernel.ai.assistant:
            # Open the AI panel or widget
            pass

    def _open_app(self, app_name):
        if self.kernel:
            self.kernel.process_manager.start_process(app_name)

    def _lock_screen(self):
        from core.lock_screen import LockScreen
        LockScreen(on_unlock=lambda: None)
