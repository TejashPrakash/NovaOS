"""Calendar application for NovaOS with event management."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox
from sdk.app import NovaApp
from core.theme import ThemeManager

# Where events are persisted
EVENTS_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "calendar_events.json"

EVENT_COLORS = [
    ("#00E5FF", "Cyan"),
    ("#FF5252", "Red"),
    ("#FF9800", "Orange"),
    ("#4CAF50", "Green"),
    ("#9C27B0", "Purple"),
    ("#FFEB3B", "Yellow"),
]


class CalendarApp(NovaApp):
    """Full calendar with month grid, event creation, and persistence."""

    APP_NAME = "Calendar"
    APP_ICON = "📅"
    DEFAULT_WIDTH = 680
    DEFAULT_HEIGHT = 560

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self._today = datetime.now()
        self._view_year = self._today.year
        self._view_month = self._today.month
        self._selected_date = None
        self._events = self._load_events()

    # ------------------------------------------------------------------ persistence
    def _load_events(self):
        try:
            if EVENTS_FILE.exists():
                with open(EVENTS_FILE, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_events(self):
        EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(EVENTS_FILE, "w") as f:
            json.dump(self._events, f, indent=2)

    # ------------------------------------------------------------------ UI
    def build(self):
        # Top bar with month navigation
        top = ctk.CTkFrame(self.content, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=(12, 6))

        ctk.CTkButton(
            top, text="◀", width=36, height=36, corner_radius=8,
            fg_color="#161B22", text_color="#FFFFFF",
            hover_color="#1C2333", border_width=1, border_color="#333333",
            font=("Segoe UI", 16),
            command=self._prev_month
        ).pack(side="left")

        self.month_label = ctk.CTkLabel(
            top, text="", font=("Segoe UI", 18, "bold"),
            text_color="#FFFFFF"
        )
        self.month_label.pack(side="left", padx=12)

        ctk.CTkButton(
            top, text="▶", width=36, height=36, corner_radius=8,
            fg_color="#161B22", text_color="#FFFFFF",
            hover_color="#1C2333", border_width=1, border_color="#333333",
            font=("Segoe UI", 16),
            command=self._next_month
        ).pack(side="left")

        ctk.CTkButton(
            top, text="Today", width=60, height=32, corner_radius=8,
            fg_color="#00E5FF", text_color="#000000",
            hover_color="#00C8E8", font=("Segoe UI", 12, "bold"),
            command=self._go_today
        ).pack(side="right")

        ctk.CTkButton(
            top, text="+ Event", width=80, height=32, corner_radius=8,
            fg_color="#4CAF50", text_color="#FFFFFF",
            hover_color="#43A047", font=("Segoe UI", 12, "bold"),
            command=self._add_event_dialog
        ).pack(side="right", padx=(0, 8))

        # Calendar grid
        self.grid_frame = ctk.CTkFrame(self.content, fg_color="#0D1117", corner_radius=12)
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        # Event list panel
        self.event_panel = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=12)
        self.event_panel.pack(fill="x", padx=20, pady=(0, 12))

        self.event_title = ctk.CTkLabel(
            self.event_panel, text="Select a day to view events",
            font=("Segoe UI", 13, "bold"), text_color="#888888"
        )
        self.event_title.pack(anchor="w", padx=15, pady=(10, 4))

        self.event_list = ctk.CTkFrame(self.event_panel, fg_color="transparent")
        self.event_list.pack(fill="x", padx=15, pady=(0, 10))

        self._draw_month()

    # ------------------------------------------------------------------ month grid
    def _draw_month(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        month_names = [
            "", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self.month_label.configure(
            text=f"{month_names[self._view_month]} {self._view_year}"
        )

        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            lbl = ctk.CTkLabel(
                self.grid_frame, text=day,
                font=("Segoe UI", 11, "bold"),
                text_color="#555555"
            )
            lbl.grid(row=0, column=col, padx=2, pady=(8, 4), sticky="nsew")
            self.grid_frame.columnconfigure(col, weight=1)

        # Calculate month days
        first_day = datetime(self._view_year, self._view_month, 1)
        if self._view_month == 12:
            next_month = datetime(self._view_year + 1, 1, 1)
        else:
            next_month = datetime(self._view_year, self._view_month + 1, 1)
        num_days = (next_month - first_day).days

        # Monday=0 ... Sunday=6
        start_weekday = (first_day.weekday()) % 7

        row = 1
        col = start_weekday

        for day in range(1, num_days + 1):
            date_str = f"{self._view_year}-{self._view_month:02d}-{day:02d}"
            has_events = date_str in self._events and len(self._events[date_str]) > 0
            is_today = (
                self._view_year == self._today.year
                and self._view_month == self._today.month
                and day == self._today.day
            )

            bg = "#0D2833" if is_today else "transparent"
            border_c = "#00E5FF" if is_today else "#222222"

            cell = ctk.CTkFrame(
                self.grid_frame, fg_color=bg, corner_radius=6,
                border_width=1 if is_today else 0,
                border_color=border_c
            )
            cell.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.grid_frame.rowconfigure(row, weight=1)

            day_num = ctk.CTkLabel(
                cell, text=str(day),
                font=("Segoe UI", 13),
                text_color="#FFFFFF" if is_today else "#CCCCCC"
            )
            day_num.pack(anchor="nw", padx=6, pady=(4, 0))

            if has_events:
                dot = ctk.CTkLabel(
                    cell, text="●", font=("Segoe UI", 8),
                    text_color="#00E5FF"
                )
                dot.pack(anchor="nw", padx=8)

            # Click binds
            for widget in (cell, day_num):
                widget.bind(
                    "<Button-1>",
                    lambda e, d=date_str, dy=day: self._select_date(d, dy)
                )

            col += 1
            if col >= 7:
                col = 0
                row += 1

    def _prev_month(self):
        if self._view_month == 1:
            self._view_month = 12
            self._view_year -= 1
        else:
            self._view_month -= 1
        self._draw_month()

    def _next_month(self):
        if self._view_month == 12:
            self._view_month = 1
            self._view_year += 1
        else:
            self._view_month += 1
        self._draw_month()

    def _go_today(self):
        self._view_year = self._today.year
        self._view_month = self._today.month
        self._draw_month()

    # ------------------------------------------------------------------ date selection
    def _select_date(self, date_str, day):
        self._selected_date = date_str
        self._draw_month()  # redraw to highlight
        self._show_events(date_str)

    def _show_events(self, date_str):
        # Clear event list
        for w in self.event_list.winfo_children():
            w.destroy()

        dt = datetime.strptime(date_str, "%Y-%m-%d")
        self.event_title.configure(
            text=f"Events for {dt.strftime('%B %d, %Y')}",
            text_color="#FFFFFF"
        )

        events = self._events.get(date_str, [])
        if not events:
            ctk.CTkLabel(
                self.event_list, text="No events",
                font=("Segoe UI", 12), text_color="#555555"
            ).pack(anchor="w", pady=4)
            return

        for i, event in enumerate(events):
            row = ctk.CTkFrame(self.event_list, fg_color="#0D1117", corner_radius=6)
            row.pack(fill="x", pady=2)

            color_dot = ctk.CTkLabel(
                row, text="●", font=("Segoe UI", 12),
                text_color=event.get("color", "#00E5FF")
            )
            color_dot.pack(side="left", padx=(10, 4), pady=6)

            time_str = event.get("time", "")
            title = event.get("title", "Untitled")

            info = f"{time_str}  {title}" if time_str else title
            ctk.CTkLabel(
                row, text=info, font=("Segoe UI", 12),
                text_color="#CCCCCC"
            ).pack(side="left", padx=4, pady=6)

            del_btn = ctk.CTkButton(
                row, text="✕", width=24, height=24, corner_radius=12,
                fg_color="transparent", text_color="#FF5252",
                hover_color="#331111", font=("Segoe UI", 11),
                command=lambda d=date_str, idx=i: self._delete_event(d, idx)
            )
            del_btn.pack(side="right", padx=8)

    def _delete_event(self, date_str, index):
        if date_str in self._events and index < len(self._events[date_str]):
            self._events[date_str].pop(index)
            if not self._events[date_str]:
                del self._events[date_str]
            self._save_events()
            self._draw_month()
            self._show_events(date_str)

    # ------------------------------------------------------------------ add event
    def _add_event_dialog(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Add Event")
        dialog.geometry("380x340")
        dialog.configure(fg_color="#0D1117")
        dialog.transient(self.window)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog, text="New Event",
            font=("Segoe UI", 18, "bold"), text_color="#00E5FF"
        ).pack(pady=(15, 10))

        # Date
        ctk.CTkLabel(
            dialog, text="Date (YYYY-MM-DD)", font=("Segoe UI", 12),
            text_color="#888888"
        ).pack(anchor="w", padx=30)

        date_entry = ctk.CTkEntry(
            dialog, placeholder_text="2026-08-25", height=36,
            fg_color="#161B22", text_color="#FFFFFF",
            corner_radius=8, border_width=1, border_color="#333333",
            font=("Segoe UI", 13)
        )
        date_entry.pack(fill="x", padx=30, pady=(2, 8))

        # Pre-fill with selected date or today
        if self._selected_date:
            date_entry.insert(0, self._selected_date)
        else:
            date_entry.insert(0, self._today.strftime("%Y-%m-%d"))

        # Time
        ctk.CTkLabel(
            dialog, text="Time (HH:MM, optional)", font=("Segoe UI", 12),
            text_color="#888888"
        ).pack(anchor="w", padx=30)

        time_entry = ctk.CTkEntry(
            dialog, placeholder_text="14:30", height=36,
            fg_color="#161B22", text_color="#FFFFFF",
            corner_radius=8, border_width=1, border_color="#333333",
            font=("Segoe UI", 13)
        )
        time_entry.pack(fill="x", padx=30, pady=(2, 8))

        # Title
        ctk.CTkLabel(
            dialog, text="Title", font=("Segoe UI", 12),
            text_color="#888888"
        ).pack(anchor="w", padx=30)

        title_entry = ctk.CTkEntry(
            dialog, placeholder_text="Meeting", height=36,
            fg_color="#161B22", text_color="#FFFFFF",
            corner_radius=8, border_width=1, border_color="#333333",
            font=("Segoe UI", 13)
        )
        title_entry.pack(fill="x", padx=30, pady=(2, 8))

        # Color
        ctk.CTkLabel(
            dialog, text="Color", font=("Segoe UI", 12),
            text_color="#888888"
        ).pack(anchor="w", padx=30)

        color_var = ctk.StringVar(value="#00E5FF")
        color_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        color_frame.pack(fill="x", padx=30, pady=(2, 8))

        for color, name in EVENT_COLORS:
            btn = ctk.CTkRadioButton(
                color_frame, text="", variable=color_var,
                value=color, fg_color=color,
                hover_color=color, border_color="#555555",
                width=24, height=24
            )
            btn.pack(side="left", padx=4)

        def save():
            date_val = date_entry.get().strip()
            title_val = title_entry.get().strip()
            time_val = time_entry.get().strip()
            color_val = color_var.get()

            if not date_val or not title_val:
                messagebox.showwarning("Missing", "Date and title are required.")
                return

            # Validate date
            try:
                datetime.strptime(date_val, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid", "Date must be YYYY-MM-DD.")
                return

            event = {"title": title_val, "time": time_val, "color": color_val}
            self._events.setdefault(date_val, []).append(event)
            self._save_events()
            self._draw_month()
            if self._selected_date == date_val:
                self._show_events(date_val)
            dialog.destroy()

        ctk.CTkButton(
            dialog, text="Save Event", height=38, corner_radius=8,
            fg_color="#00E5FF", text_color="#000000",
            hover_color="#00C8E8", font=("Segoe UI", 14, "bold"),
            command=save
        ).pack(pady=(10, 15))
