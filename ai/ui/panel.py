"""AI Panel UI component for NovaOS."""

import customtkinter as ctk
from ai.assistant import Assistant


class AIPanel(ctk.CTkFrame):
    """Glassmorphism AI Panel for NovaOS desktop."""

    def __init__(self, master, assistant: Assistant, on_close=None, **kwargs):
        super().__init__(
            master,
            width=400,
            height=500,
            fg_color="#161B22",
            corner_radius=20,
            **kwargs
        )
        self.assistant = assistant
        self._on_close_callback = on_close
        self._setup_ui()

    def _setup_ui(self):
        """Setup the AI panel UI."""
        # Header
        self.header = ctk.CTkFrame(
            self,
            fg_color="#0D1117",
            corner_radius=15,
            height=60
        )
        self.header.pack(fill="x", padx=10, pady=10)

        title = ctk.CTkLabel(
            self.header,
            text="◈ Nova AI",
            font=("Segoe UI", 18, "bold"),
            text_color="#00E5FF"
        )
        title.pack(side="left", pady=15, padx=15)

        # Close button
        close_btn = ctk.CTkButton(
            self.header, text="✕", width=30, height=30,
            fg_color="transparent", text_color="#666666",
            hover_color="#C62828", corner_radius=15,
            font=("Segoe UI", 14, "bold"),
            command=self._close
        )
        close_btn.pack(side="right", padx=10, pady=15)

        # Chat area
        self.chat_frame = ctk.CTkFrame(
            self,
            fg_color="#0D1117",
            corner_radius=15
        )
        self.chat_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.chat_display = ctk.CTkTextbox(
            self.chat_frame,
            fg_color="transparent",
            text_color="#BBBBBB",
            font=("Segoe UI", 11),
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)

        # Input area
        self.input_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.input_frame.pack(fill="x", padx=10, pady=10)

        self.user_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ask Nova anything...",
            fg_color="#0D1117",
            text_color="#BBBBBB",
            placeholder_text_color="#666666",
            corner_radius=25,
            height=40
        )
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self._handle_input)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="◈",
            width=50,
            height=40,
            fg_color="#00E5FF",
            text_color="black",
            hover_color="#00C8E8",
            corner_radius=25,
            command=self._handle_input
        )
        self.send_button.pack(side="right")

    def _close(self):
        """Close this panel."""
        try:
            if self._on_close_callback:
                self._on_close_callback()
            self.destroy()
        except Exception:
            pass

    def _handle_input(self, event=None):
        """Handle user input."""
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        # Add user message
        self._add_message("You", user_text)
        self.user_input.delete(0, "end")

        # Get AI response
        response = self.assistant.ask(user_text)

        # Add AI response
        self._add_message("Nova", response)

    def _add_message(self, sender: str, message: str):
        """Add message to chat display."""
        self.chat_display.configure(state="normal")

        color = "#00E5FF" if sender == "Nova" else "#BBBBBB"
        self.chat_display.insert("end", f"{sender}: {message}\n\n", ("message",))
        self.chat_display.tag_config("message", foreground=color)

        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")