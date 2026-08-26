"""Smart AI notification system for NovaOS — generates contextual notifications."""

import time
from datetime import datetime

import customtkinter as ctk
from core.theme import ThemeManager


class SmartNotificationManager:
    """Generates and manages AI-powered smart notifications."""

    def __init__(self, desktop, kernel=None):
        self.desktop = desktop
        self.kernel = kernel
        self.theme = ThemeManager()
        self._last_notification_time = 0
        self._notification_cooldown = 300  # 5 minutes between notifications
        self._shown_today = set()

    def check_and_notify(self):
        """Check if any smart notifications should be shown."""
        now = time.time()
        if now - self._last_notification_time < self._notification_cooldown:
            return

        hour = datetime.now().hour
        notifications = self._get_smart_notifications(hour)

        for notification in notifications:
            key = f"{notification['title']}_{hour}"
            if key not in self._shown_today:
                self._show_notification(notification)
                self._shown_today.add(key)
                self._last_notification_time = now
                break

    def _get_smart_notifications(self, hour):
        """Generate notifications based on time of day."""
        notifications = []

        if hour == 9:
            notifications.append({
                "icon": "☀️",
                "title": "Good Morning!",
                "message": "Ready to start your day? Check your Calendar for today's events.",
                "action": "Calendar"
            })
        elif hour == 12:
            notifications.append({
                "icon": "🍽️",
                "title": "Lunch Time",
                "message": "Take a break! The Music Player has some great tunes.",
                "action": "Music Player"
            })
        elif hour == 17:
            notifications.append({
                "icon": "📊",
                "title": "End of Day",
                "message": "Check your system health before wrapping up.",
                "action": "System Monitor"
            })
        elif hour == 22:
            notifications.append({
                "icon": "🌙",
                "title": "Night Mode",
                "message": "Consider locking your screen. Press Ctrl+Shift+L.",
                "action": None
            })

        # System-based notifications
        if self.kernel:
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=0)
                if cpu > 90:
                    notifications.append({
                        "icon": "⚠️",
                        "title": "High CPU Usage",
                        "message": f"CPU is at {cpu:.0f}%. Consider closing unused apps.",
                        "action": "System Monitor"
                    })

                ram = psutil.virtual_memory()
                if ram.percent > 85:
                    notifications.append({
                        "icon": "💾",
                        "title": "High Memory Usage",
                        "message": f"RAM is at {ram.percent:.0f}%. {ram.available // (1024**2)} MB free.",
                        "action": "System Monitor"
                    })
            except Exception:
                pass

        return notifications

    def _show_notification(self, notification):
        """Display a smart notification popup."""
        frame = ctk.CTkFrame(
            self.desktop.get_widget_layer(),
            width=360,
            height=90,
            fg_color="#1A1F2B",
            corner_radius=14,
            border_width=1,
            border_color="#00E5FF"
        )

        # Position at top-right
        frame.place(relx=0.98, rely=0.05, anchor="ne")

        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=14, pady=10)

        # Header
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkLabel(
            header, text=notification["icon"],
            font=("Segoe UI Emoji", 18)
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            header, text=notification["title"],
            font=("Segoe UI", 12, "bold"),
            text_color="#00E5FF"
        ).pack(side="left")

        # Close button
        ctk.CTkButton(
            header, text="✕", width=22, height=22,
            fg_color="transparent", text_color="#666666",
            hover_color="#331111", corner_radius=11,
            font=("Segoe UI", 10),
            command=lambda: self._dismiss(frame)
        ).pack(side="right")

        # Message
        ctk.CTkLabel(
            content, text=notification["message"],
            font=("Segoe UI", 11),
            text_color="#BBBBBB",
            wraplength=310,
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))

        # Action button
        if notification.get("action"):
            def open_action(action=notification["action"]):
                self._dismiss(frame)
                if self.kernel:
                    self.kernel.process_manager.start_process(action)

            ctk.CTkButton(
                content, text=f"Open {notification['action']}",
                height=24, width=100,
                fg_color="#00E5FF", text_color="#000000",
                hover_color="#00C8E8", corner_radius=6,
                font=("Segoe UI", 10, "bold"),
                command=open_action
            ).pack(anchor="e", pady=(4, 0))

        # Auto-dismiss after 8 seconds
        frame.after(8000, lambda: self._dismiss(frame))

    def _dismiss(self, frame):
        try:
            frame.destroy()
        except Exception:
            pass

    def reset_daily(self):
        """Reset daily notification tracking (call at midnight)."""
        self._shown_today.clear()
