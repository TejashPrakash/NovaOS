import customtkinter as ctk
from core.theme import ThemeManager


class AIAssistantWidget(ctk.CTkFrame):
    """Always-visible AI assistant widget on the desktop."""

    def __init__(self, master, assistant, **kwargs):
        self.theme = ThemeManager()
        super().__init__(
            master,
            width=320,
            height=420,
            fg_color="#0D1117",
            corner_radius=16,
            border_width=2,
            border_color="#00E5FF",
            **kwargs
        )
        self.assistant = assistant
        self.pack_propagate(False)
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 5))

        ctk.CTkLabel(
            header, text="◈ Nova",
            font=("Segoe UI", 16, "bold"),
            text_color="#00E5FF"
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="AI Assistant",
            font=("Segoe UI", 12),
            text_color="#666666"
        ).pack(side="left", padx=(5, 0))

        # Quick actions
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=12, pady=(0, 5))

        quick_actions = [
            ("⏰ Time", "What time is it?"),
            ("📅 Date", "What is today's date?"),
            ("📊 Status", "Show system status"),
            ("🌤 Weather", "Weather in my location"),
        ]

        for text, query in quick_actions:
            btn = ctk.CTkButton(
                actions_frame, text=text, width=72, height=28,
                fg_color="#161B22", hover_color="#252B3B",
                text_color="#BBBBBB", corner_radius=8,
                font=("Segoe UI", 10),
                command=lambda q=query: self._quick_ask(q)
            )
            btn.pack(side="left", padx=2, pady=2)

        # Chat area
        self.chat_area = ctk.CTkTextbox(
            self,
            fg_color="#0A0E14",
            text_color="#BBBBBB",
            font=("Segoe UI", 12),
            wrap="word",
            state="disabled",
            corner_radius=8
        )
        self.chat_area.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self._add_system_message("Hello! I'm Nova, your AI assistant. Ask me anything!")

        # Input
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.user_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask Nova...",
            fg_color="#161B22",
            text_color="#FFFFFF",
            font=("Segoe UI", 12),
            corner_radius=20,
            border_width=1,
            border_color="#00E5FF"
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", self._send_message)

        self.send_btn = ctk.CTkButton(
            input_frame, text="◈", width=38, height=38,
            fg_color="#00E5FF", text_color="black",
            hover_color="#00C8E8", corner_radius=20,
            font=("Segoe UI", 14, "bold"),
            command=self._send_message
        )
        self.send_btn.pack(side="right")

    def _send_message(self, event=None):
        text = self.user_input.get().strip()
        if not text or self.assistant is None:
            return

        self.user_input.delete(0, "end")
        self._add_user_message(text)

        # Show thinking
        self._add_system_message("Thinking...")

        # Get response (safe for GUI thread)
        try:
            response = self.assistant.ask(text)
            # Remove "Thinking..." and add real response
            self._remove_last_line()
            self._add_ai_message(response)
        except Exception as e:
            self._remove_last_line()
            self._add_system_message(f"Error: {e}")

    def _quick_ask(self, query):
        self.user_input.delete(0, "end")
        self.user_input.insert(0, query)
        self._send_message()

    def _add_user_message(self, text):
        self._write(f"👤 You: {text}\n\n", "#FFFFFF")

    def _add_ai_message(self, text):
        self._write(f"◈ Nova: {text}\n\n", "#00E5FF")

    def _add_system_message(self, text):
        self._write(f"  {text}\n", "#666666")

    def _remove_last_line(self):
        self.chat_area.configure(state="normal")
        content = self.chat_area.get("1.0", "end-1c")
        lines = content.rsplit("\n\n", 1)
        if len(lines) > 1:
            self.chat_area.delete("1.0", "end")
            self.chat_area.insert("1.0", lines[0] + "\n\n")
        self.chat_area.configure(state="disabled")

    def _write(self, text, color):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", text, ("msg",))
        self.chat_area.tag_config("msg", foreground=color)
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")