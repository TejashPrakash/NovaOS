"""Collapsible AI assistant widget for the NovaOS desktop.

Default state: small floating orb (◈ icon).
Expanded state: full chat panel with quick actions.
"""

import customtkinter as ctk
from core.theme import ThemeManager


class AIAssistantWidget(ctk.CTkFrame):
    """Collapsible AI widget — orb when collapsed, chat when expanded."""

    ORB_SIZE = 52
    PANEL_WIDTH = 320
    PANEL_HEIGHT = 420

    def __init__(self, master, assistant, **kwargs):
        self.theme = ThemeManager()
        super().__init__(
            master,
            width=self.ORB_SIZE,
            height=self.ORB_SIZE,
            fg_color="#0D1117",
            corner_radius=26,
            border_width=2,
            border_color="#00E5FF",
            **kwargs
        )
        self.assistant = assistant
        self.pack_propagate(False)
        self._expanded = False
        self._build_orb()

    # ------------------------------------------------------------------
    # Orb (collapsed)
    # ------------------------------------------------------------------
    def _build_orb(self):
        self._orb_label = ctk.CTkLabel(
            self, text="◈",
            font=("Segoe UI Emoji", 22),
            text_color="#00E5FF"
        )
        self._orb_label.pack(expand=True)

        self.bind("<Button-1>", lambda e: self.toggle())
        self._orb_label.bind("<Button-1>", lambda e: self.toggle())

    # ------------------------------------------------------------------
    # Toggle
    # ------------------------------------------------------------------
    def toggle(self):
        if self._expanded:
            self._collapse()
        else:
            self._expand()

    def _expand(self):
        self._expanded = True
        for w in self.winfo_children():
            w.destroy()
        self.configure(
            width=self.PANEL_WIDTH,
            height=self.PANEL_HEIGHT,
            corner_radius=16,
            border_color="#00E5FF"
        )
        self._build_chat()

    def _collapse(self):
        self._expanded = False
        for w in self.winfo_children():
            w.destroy()
        self.configure(
            width=self.ORB_SIZE,
            height=self.ORB_SIZE,
            corner_radius=26,
            border_color="#00E5FF"
        )
        self._build_orb()

    # ------------------------------------------------------------------
    # Chat panel
    # ------------------------------------------------------------------
    def _build_chat(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            header, text="◈ Nova",
            font=("Segoe UI", 14, "bold"),
            text_color="#00E5FF"
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="AI Assistant",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left", padx=(4, 0))

        close_btn = ctk.CTkButton(
            header, text="✕", width=26, height=26,
            fg_color="transparent", text_color="#666666",
            hover_color="#1C2333", corner_radius=13,
            font=("Segoe UI", 11),
            command=self._collapse
        )
        close_btn.pack(side="right")

        # Quick actions
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=(0, 4))

        for text, query in [
            ("⏰ Time", "What time is it?"),
            ("📅 Date", "What is today's date?"),
            ("📊 Status", "Show system status"),
            ("🌤 Weather", "Weather in my location"),
        ]:
            ctk.CTkButton(
                actions_frame, text=text, width=68, height=26,
                fg_color="#161B22", hover_color="#252B3B",
                text_color="#BBBBBB", corner_radius=6,
                font=("Segoe UI", 9),
                command=lambda q=query: self._quick_ask(q)
            ).pack(side="left", padx=2, pady=2)

        # Chat area
        self.chat_area = ctk.CTkTextbox(
            self, fg_color="#0A0E14", text_color="#BBBBBB",
            font=("Segoe UI", 12), wrap="word",
            state="disabled", corner_radius=8
        )
        self.chat_area.pack(fill="both", expand=True, padx=8, pady=(0, 4))
        self._add_system("Hello! I'm Nova, your AI assistant. Ask me anything!")

        # Input
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=8, pady=(0, 8))

        self.user_input = ctk.CTkEntry(
            input_frame, placeholder_text="Ask Nova...",
            fg_color="#161B22", text_color="#FFFFFF",
            font=("Segoe UI", 11), corner_radius=18,
            border_width=1, border_color="#00E5FF"
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.user_input.bind("<Return>", self._send)

        ctk.CTkButton(
            input_frame, text="◈", width=34, height=34,
            fg_color="#00E5FF", text_color="black",
            hover_color="#00C8E8", corner_radius=17,
            font=("Segoe UI", 13, "bold"),
            command=self._send
        ).pack(side="right")

    # ------------------------------------------------------------------
    # Chat logic
    # ------------------------------------------------------------------
    def _send(self, event=None):
        text = self.user_input.get().strip()
        if not text or self.assistant is None:
            return
        self.user_input.delete(0, "end")
        self._add_user(text)
        self._add_system("Thinking...")
        try:
            response = self.assistant.ask(text)
            self._remove_last()
            self._add_ai(response)
        except Exception as e:
            self._remove_last()
            self._add_system(f"Error: {e}")

    def _quick_ask(self, query):
        self.user_input.delete(0, "end")
        self.user_input.insert(0, query)
        self._send()

    def _add_user(self, text):
        self._write(f"👤 You: {text}\n\n", "#FFFFFF")

    def _add_ai(self, text):
        self._write(f"◈ Nova: {text}\n\n", "#00E5FF")

    def _add_system(self, text):
        self._write(f"  {text}\n", "#666666")

    def _remove_last(self):
        self.chat_area.configure(state="normal")
        content = self.chat_area.get("1.0", "end-1c")
        parts = content.rsplit("\n\n", 1)
        if len(parts) > 1:
            self.chat_area.delete("1.0", "end")
            self.chat_area.insert("1.0", parts[0] + "\n\n")
        self.chat_area.configure(state="disabled")

    def _write(self, text, color):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", text, ("msg",))
        self.chat_area.tag_config("msg", foreground=color)
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")
