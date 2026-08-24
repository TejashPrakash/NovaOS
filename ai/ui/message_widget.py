import customtkinter as ctk
from datetime import datetime


class MessageWidget(ctk.CTkFrame):
    """Widget for displaying chat messages in the assistant UI."""
    
    def __init__(self, master, text: str = "", role: str = "user", **kwargs):
        super().__init__(master, **kwargs)
        self.text = text
        self.role = role
        self.timestamp = datetime.now()
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the message widget UI."""
        # Configure frame based on role
        if self.role == "user":
            self.configure(fg_color="#2B2B2B", corner_radius=10)
        else:  # assistant
            self.configure(fg_color="#1A1A2E", corner_radius=10)
        
        # Message content
        self.message_label = ctk.CTkLabel(
            self,
            text=self.text,
            wraplength=400,
            justify="left",
            anchor="nw",
            font=("Segoe UI", 12),
            text_color="white" if self.role == "user" else "#00E5FF"
        )
        self.message_label.pack(padx=15, pady=10, anchor="w")
        
        # Timestamp
        time_str = self.timestamp.strftime("%H:%M")
        self.timestamp_label = ctk.CTkLabel(
            self,
            text=time_str,
            font=("Segoe UI", 9),
            text_color="#666666"
        )
        self.timestamp_label.pack(padx=15, pady=(0, 8), anchor="e")
    
    def update_text(self, text: str):
        """Update the message text."""
        self.text = text
        self.message_label.configure(text=text)
    
    def get_text(self) -> str:
        """Get the message text."""
        return self.text
    
    def get_role(self) -> str:
        """Get the message role."""
        return self.role