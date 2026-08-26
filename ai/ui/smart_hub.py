"""AI-powered smart suggestions widget for the NovaOS desktop."""

import time
from datetime import datetime

import customtkinter as ctk
from core.theme import ThemeManager


class SmartSuggestionsWidget(ctk.CTkFrame):
    """Always-visible AI widget that shows contextual suggestions based on time, usage, and context."""

    def __init__(self, master, kernel=None, **kwargs):
        super().__init__(
            master,
            width=340,
            height=480,
            fg_color="#0D1117",
            corner_radius=16,
            border_width=1,
            border_color="#222222",
            **kwargs
        )
        self.kernel = kernel
        self.theme = ThemeManager()
        self.pack_propagate(False)
        self._build_ui()
        self._refresh_suggestions()
        self._auto_refresh()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 6))

        ctk.CTkLabel(
            header, text="◈ Nova AI",
            font=("Segoe UI", 15, "bold"),
            text_color="#00E5FF"
        ).pack(side="left")

        ctk.CTkLabel(
            header, text="Smart Hub",
            font=("Segoe UI", 11),
            text_color="#666666"
        ).pack(side="left", padx=(6, 0))

        # Time-based greeting
        self.greeting_label = ctk.CTkLabel(
            self, text="",
            font=("Segoe UI", 13),
            text_color="#BBBBBB",
            wraplength=300
        )
        self.greeting_label.pack(anchor="w", padx=14, pady=(4, 8))

        # Suggestions container
        self.suggestions_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.suggestions_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Quick actions row
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=10, pady=(0, 10))

        quick_actions = [
            ("📝", "New Note", self._action_new_note),
            ("📅", "Add Event", self._action_add_event),
            ("🌤", "Weather", self._action_weather),
            ("📊", "System", self._action_system),
        ]

        for icon, label, callback in quick_actions:
            btn = ctk.CTkButton(
                actions_frame, text=f"{icon}\n{label}",
                width=70, height=55,
                fg_color="#161B22", hover_color="#1C2333",
                text_color="#BBBBBB", corner_radius=10,
                border_width=1, border_color="#333333",
                font=("Segoe UI", 10),
                command=callback
            )
            btn.pack(side="left", padx=3, expand=True, fill="x")

    def _refresh_suggestions(self):
        """Generate contextual suggestions based on time and state."""
        for w in self.suggestions_frame.winfo_children():
            w.destroy()

        hour = datetime.now().hour
        suggestions = self._get_contextual_suggestions(hour)

        # Greeting
        greeting = self._get_greeting(hour)
        self.greeting_label.configure(text=greeting)

        # Build suggestion cards
        for icon, title, desc, priority in suggestions:
            self._add_suggestion_card(icon, title, desc, priority)

    def _get_greeting(self, hour):
        if hour < 6:
            return "🌙 Working late? Stay focused!"
        elif hour < 12:
            return "☀️ Good morning! Ready to be productive?"
        elif hour < 17:
            return "🌤 Good afternoon! Keep it up!"
        elif hour < 21:
            return "🌆 Good evening! Winding down?"
        else:
            return "🌙 Night mode. Take a break!"

    def _get_contextual_suggestions(self, hour):
        suggestions = []

        # Time-based suggestions
        if 9 <= hour < 12:
            suggestions.append(("📅", "Check your calendar", "Start your day by reviewing today's events", "high"))
            suggestions.append(("🌤", "Morning weather", "Check today's forecast before heading out", "medium"))
        elif 12 <= hour < 14:
            suggestions.append(("🎵", "Lunch break music", "Open Music Player for some relaxation", "medium"))
            suggestions.append(("📝", "Quick notes", "Jot down morning meeting notes", "low"))
        elif 14 <= hour < 17:
            suggestions.append(("📊", "System health check", "Monitor CPU and memory usage", "medium"))
            suggestions.append(("🌐", "Research time", "Use the Browser for afternoon research", "low"))
        elif 17 <= hour < 21:
            suggestions.append(("📅", "Plan tomorrow", "Add tomorrow's tasks to Calendar", "high"))
            suggestions.append(("🎵", "Evening vibes", "Relax with the Music Player", "medium"))
        else:
            suggestions.append(("📝", "Daily journal", "Write a quick note about today", "medium"))
            suggestions.append(("🔒", "Lock your screen", "Secure your desktop with Ctrl+Shift+L", "low"))

        # Always suggest
        suggestions.append(("🤖", "Ask Nova anything", "I can help with apps, notes, weather, and more", "always"))
        suggestions.append(("⚙️", "Customize themes", "Switch between Cyberpunk, Neon, Sunset, or Ocean", "low"))

        return suggestions

    def _add_suggestion_card(self, icon, title, desc, priority):
        """Add a suggestion card to the scrollable frame."""
        colors = {
            "high": "#0D2833",
            "medium": "#161B22",
            "low": "#0D1117",
            "always": "#0D1117"
        }
        border_colors = {
            "high": "#00E5FF",
            "medium": "#333333",
            "low": "#222222",
            "always": "#7B61FF"
        }

        card = ctk.CTkFrame(
            self.suggestions_frame,
            fg_color=colors.get(priority, "#161B22"),
            corner_radius=10,
            border_width=1,
            border_color=border_colors.get(priority, "#333333")
        )
        card.pack(fill="x", pady=4)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(8, 2))

        ctk.CTkLabel(
            header, text=icon, font=("Segoe UI Emoji", 16)
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            header, text=title,
            font=("Segoe UI", 12, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left")

        ctk.CTkLabel(
            card, text=desc,
            font=("Segoe UI", 11),
            text_color="#888888",
            wraplength=280,
            anchor="w"
        ).pack(anchor="w", padx=10, pady=(0, 8))

    # ------------------------------------------------------------------ quick actions
    def _action_new_note(self):
        if self.kernel:
            self.kernel.process_manager.start_process("Notes")

    def _action_add_event(self):
        if self.kernel:
            self.kernel.process_manager.start_process("Calendar")

    def _action_weather(self):
        if self.kernel:
            self.kernel.process_manager.start_process("Weather")

    def _action_system(self):
        if self.kernel:
            self.kernel.process_manager.start_process("System Monitor")

    def _auto_refresh(self):
        """Refresh suggestions every 5 minutes."""
        try:
            self.after(300000, self._auto_refresh)
            self._refresh_suggestions()
        except Exception:
            pass
