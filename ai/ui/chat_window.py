import customtkinter as ctk
from ai.ui.message_widget import MessageWidget


class ChatWindow(ctk.CTkToplevel):
    """Chat window for the NovaOS assistant."""
    
    def __init__(self, assistant, title: str = "NovaOS Assistant", **kwargs):
        super().__init__(**kwargs)
        self.title(title)
        self.geometry("500x600")
        self.assistant = assistant
        
        self._setup_ui()
        self._setup_events()
    
    def _setup_ui(self):
        """Setup the chat window UI."""
        # Configure window
        self.configure(fg_color="#1E1E2E")
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Message history frame (scrollable)
        self.messages_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            label_text="Conversation",
            label_font=("Segoe UI", 14, "bold")
        )
        self.messages_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B", corner_radius=10)
        self.input_frame.pack(fill="x", pady=(0, 0))
        
        # Message input
        self.message_input = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ask Nova something...",
            fg_color="transparent",
            border_color="#444444",
            text_color="white",
            placeholder_text_color="#888888",
            height=40
        )
        self.message_input.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=80,
            height=40,
            fg_color="#00E5FF",
            hover_color="#00C8E8",
            text_color="black",
            corner_radius=8,
            command=self.send_message
        )
        self.send_button.pack(side="right", padx=10, pady=10)
    
    def _setup_events(self):
        """Setup keyboard events."""
        self.bind("<Return>", lambda e: self.send_message())
        self.message_input.bind("<Return>", lambda e: self.send_message())
    
    def send_message(self):
        """Send a message to the assistant."""
        message = self.message_input.get().strip()
        if not message:
            return
        
        # Add user message to chat
        self._add_message(message, "user")
        
        # Clear input
        self.message_input.delete(0, "end")
        
        # Get assistant response
        if self.assistant:
            response = self.assistant.ask(message)
            self._add_message(response, "assistant")
        else:
            self._add_message("Assistant not available", "assistant")
    
    def _add_message(self, text: str, role: str):
        """Add a message to the chat history."""
        message_widget = MessageWidget(
            self.messages_frame,
            text=text,
            role=role
        )
        message_widget.pack(fill="x", pady=5, padx=5)
        
        # Scroll to bottom
        self.messages_frame._parent_canvas.yview_moveto(1.0)
    
    def clear_chat(self):
        """Clear all messages from the chat."""
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
    
    def show(self):
        """Show the chat window."""
        self.deiconify()
        self.lift()
    
    def hide(self):
        """Hide the chat window."""
        self.withdraw()