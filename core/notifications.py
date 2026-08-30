import customtkinter as ctk
from dataclasses import dataclass
from typing import Optional, Callable
from datetime import datetime, timedelta


@dataclass
class Notification:
    """Notification data structure."""
    title: str
    message: str
    icon: str = "🔔"
    duration: int = 5  # seconds
    callback: Optional[Callable] = None


class NotificationSystem:
    """Notification system for NovaOS."""
    
    def __init__(self, desktop):
        self.desktop = desktop
        self.notifications = []
        self.current_notification = None
        
    def show(self, notification: Notification):
        """Show a notification."""
        self.notifications.append(notification)
        self._display_notification(notification)
        
    def _display_notification(self, notification: Notification):
        """Display notification popup."""
        if self.current_notification:
            self._hide_current()
            
        # Create notification frame
        self.current_notification = ctk.CTkFrame(
            self.desktop.get_widget_layer(),
            width=350,
            height=80,
            fg_color="#1A1F2B",
            corner_radius=12,
            border_width=1,
            border_color="#00E5FF"
        )
        
        # Position at top-center (avoids AI orb at top-right and Smart Hub at top-left)
        self.current_notification.place(
            relx=0.5,
            rely=0.05,
            anchor="n"
        )
        
        # Content
        content_frame = ctk.CTkFrame(
            self.current_notification,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Icon and title
        header_frame = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x")
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=notification.icon,
            font=("Segoe UI", 20)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=notification.title,
            font=("Segoe UI", 12, "bold"),
            text_color="#00E5FF"
        )
        title_label.pack(side="left")
        
        # Message
        message_label = ctk.CTkLabel(
            content_frame,
            text=notification.message,
            font=("Segoe UI", 10),
            text_color="#BBBBBB",
            wraplength=300
        )
        message_label.pack(pady=(5, 0))
        
        # Auto-hide after duration
        self.desktop.root.after(notification.duration * 1000, self._hide_current)
        
    def _hide_current(self):
        """Hide current notification."""
        if self.current_notification:
            self.current_notification.destroy()
            self.current_notification = None