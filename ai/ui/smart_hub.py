"""Collapsible AI smart suggestions widget for the NovaOS desktop.

Default state: small floating pill (logo + label).
Expanded state: full suggestion panel with quick actions.
Click the pill to toggle.
"""

from datetime import datetime
import customtkinter as ctk
from core.theme import ThemeManager


class SmartSuggestionsWidget(ctk.CTkFrame):
    """Collapsible smart hub — pill when collapsed, full panel when expanded."""

    PILL_WIDTH = 160
    PILL_HEIGHT = 44
    PANEL_WIDTH = 300
    PANEL_HEIGHT = 420

    def __init__(self, master, kernel=None, on_toggle=None, start_menu_ref=None, **kwargs):
        super().__init__(
            master,
            width=self.PILL_WIDTH,
            height=self.PILL_HEIGHT,
            fg_color="#0D1117",
            corner_radius=22,
            border_width=1,
            border_color="#1E2A3A",
            **kwargs
        )
        self.kernel = kernel
        self.start_menu_ref = start_menu_ref
        self.theme = ThemeManager()
        self.pack_propagate(False)
        self._expanded = False
        self._on_toggle = on_toggle
        self._build_pill()
        self._auto_refresh()

    # ------------------------------------------------------------------
    # Collapsed pill
    # ------------------------------------------------------------------
    def _build_pill(self):
        self._pill_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._pill_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self._pill_frame, text="◈",
            font=("Segoe UI Emoji", 18),
            text_color="#00E5FF"
        ).pack(side="left", padx=(12, 4), pady=8)

        ctk.CTkLabel(
            self._pill_frame, text="Smart Hub",
            font=("Segoe UI", 12, "bold"),
            text_color="#AAAAAA"
        ).pack(side="left", padx=(0, 12), pady=8)

        self.bind("<Button-1>", self._on_pill_click)
        self._pill_frame.bind("<Button-1>", self._on_pill_click)
        for child in self._pill_frame.winfo_children():
            child.bind("<Button-1>", self._on_pill_click)

    def _on_pill_click(self, event=None):
        """Handle pill click — prevent event propagation."""
        self.toggle()
        if event:
            return "break"

    # ------------------------------------------------------------------
    # Toggle expand / collapse
    # ------------------------------------------------------------------
    def toggle(self, event=None):
        if self._expanded:
            self._collapse()
        else:
            self._expand()
        if event:
            return "break"

    def _expand(self):
        """Expand to full panel."""
        self._expanded = True
        self._pill_frame.pack_forget()
        self.configure(
            width=self.PANEL_WIDTH,
            height=self.PANEL_HEIGHT,
            corner_radius=16,
            border_color="#00E5FF"
        )
        self._build_panel()
        # Close start menu if open
        if self.start_menu_ref:
            try:
                if self.start_menu_ref.winfo_ismapped():
                    self.start_menu_ref.hide()
            except Exception:
                pass
        if self._on_toggle:
            self._on_toggle(True)

    def _collapse(self):
        """Collapse back to pill."""
        self._expanded = False
        # Destroy panel children
        for w in self.winfo_children():
            w.destroy()
        self.configure(
            width=self.PILL_WIDTH,
            height=self.PILL_HEIGHT,
            corner_radius=22,
            border_color="#1E2A3A"
        )
        self._build_pill()
        if self._on_toggle:
            self._on_toggle(False)

    # ------------------------------------------------------------------
    # Full panel
    # ------------------------------------------------------------------
    def _build_panel(self):
        # Header with close
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            header, text="◈ Nova AI",
            font=("Segoe UI", 14, "bold"),
            text_color="#00E5FF"
        ).pack(side="left")

        close_btn = ctk.CTkButton(
            header, text="✕", width=28, height=28,
            fg_color="transparent", text_color="#666666",
            hover_color="#1C2333", corner_radius=14,
            font=("Segoe UI", 12),
            command=self._collapse
        )
        close_btn.pack(side="right")

        # Greeting
        hour = datetime.now().hour
        greeting = self._get_greeting(hour)
        ctk.CTkLabel(
            self, text=greeting,
            font=("Segoe UI", 12),
            text_color="#999999",
            wraplength=270
        ).pack(anchor="w", padx=14, pady=(2, 8))

        # Suggestions
        suggestions_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        suggestions_frame.pack(fill="both", expand=True, padx=8, pady=(0, 6))

        suggestions = self._get_suggestions(hour)
        for icon, title, desc, priority, cb in suggestions:
            self._add_card(suggestions_frame, icon, title, desc, priority, cb)

        # Quick actions
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=8, pady=(0, 8))

        for icon, label, cb in [
            ("📝", "Note", self._act("Notes")),
            ("📅", "Event", self._act("Calendar")),
            ("🌤", "Weather", self._act("Weather")),
            ("📊", "System", self._act("System Monitor")),
        ]:
            ctk.CTkButton(
                actions, text=f"{icon}\n{label}",
                width=60, height=48,
                fg_color="#161B22", hover_color="#1C2333",
                text_color="#BBBBBB", corner_radius=8,
                border_width=1, border_color="#2A2A2A",
                font=("Segoe UI", 9),
                command=cb
            ).pack(side="left", padx=2, expand=True, fill="x")

    def _add_card(self, parent, icon, title, desc, priority, callback=None):
        bc = {"high": "#00E5FF", "always": "#7B61FF"}.get(priority, "#222222")
        card = ctk.CTkFrame(
            parent, fg_color="#161B22",
            corner_radius=8, border_width=1, border_color=bc
        )
        card.pack(fill="x", pady=3)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=(6, 1))
        ctk.CTkLabel(row, text=icon, font=("Segoe UI Emoji", 14)).pack(side="left", padx=(0, 4))
        ctk.CTkLabel(row, text=title, font=("Segoe UI", 11, "bold"), text_color="#FFFFFF").pack(side="left")

        desc_label = ctk.CTkLabel(
            card, text=desc,
            font=("Segoe UI", 10), text_color="#777777",
            wraplength=250, anchor="w"
        )
        desc_label.pack(anchor="w", padx=8, pady=(0, 6))

        # Make the entire card clickable
        if callback:
            for widget in (card, row, desc_label):
                widget.bind("<Button-1>", lambda e: callback())
                widget.bind("<Enter>", lambda e: card.configure(border_color="#00E5FF"))
                widget.bind("<Leave>", lambda e: card.configure(border_color=bc))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _act(self, app_name):
        def _launch():
            if self.kernel:
                self.kernel.process_manager.start_process(app_name)
        return _launch

    def _lock_screen(self):
        """Lock the screen."""
        from core.lock_screen import LockScreen
        LockScreen(on_unlock=lambda: None)

    def _open_ai(self):
        """Open the AI assistant panel."""
        if self.kernel and hasattr(self.kernel, 'desktop'):
            self.kernel.desktop.toggle_ai_panel(self.kernel.ai.assistant if hasattr(self.kernel, 'ai') and self.kernel.ai else None)

    def _get_greeting(self, hour):
        if hour < 6:
            return "🌙 Working late? Stay focused!"
        elif hour < 12:
            return "☀️ Good morning! Ready to be productive?"
        elif hour < 17:
            return "🌤 Good afternoon! Keep it up!"
        elif hour < 21:
            return "🌆 Good evening! Winding down?"
        return "🌙 Night mode. Take a break!"

    def _get_suggestions(self, hour):
        """Return list of (icon, title, desc, priority, callback)."""
        s = []
        if 9 <= hour < 12:
            s.append(("📅", "Check calendar", "Review today's events", "high", self._act("Calendar")))
            s.append(("🌤", "Morning weather", "Check the forecast", "medium", self._act("Weather")))
        elif 12 <= hour < 14:
            s.append(("🎵", "Lunch music", "Relax with Music Player", "medium", self._act("Music Player")))
            s.append(("📝", "Quick notes", "Jot down ideas", "low", self._act("Notes")))
        elif 14 <= hour < 17:
            s.append(("📊", "System check", "Monitor CPU and RAM", "medium", self._act("System Monitor")))
            s.append(("🌐", "Research", "Use the Browser", "low", self._act("Browser")))
        elif 17 <= hour < 21:
            s.append(("📅", "Plan tomorrow", "Add tasks to Calendar", "high", self._act("Calendar")))
            s.append(("🎵", "Evening vibes", "Relax with music", "medium", self._act("Music Player")))
        else:
            s.append(("📝", "Daily journal", "Write about today", "medium", self._act("Notes")))
            s.append(("🔒", "Lock screen", "Ctrl+Shift+L", "low", self._lock_screen))

        s.append(("🤖", "Ask Nova anything", "I can help with anything", "always", self._open_ai))
        return s

    def _auto_refresh(self):
        try:
            self.after(300000, self._auto_refresh)
        except Exception:
            pass
