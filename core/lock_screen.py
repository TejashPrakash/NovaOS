"""Lock / login screen for NovaOS."""

import time
import customtkinter as ctk
from core.theme import ThemeManager
from core.sounds import sound_manager


class LockScreen(ctk.CTkToplevel):
    """Full-screen lock screen with clock, date, and password authentication."""

    # Default credentials (in production, hash these)
    DEFAULT_USERNAME = "Nova User"
    DEFAULT_PASSWORD = "nova"

    def __init__(self, on_unlock=None):
        super().__init__()

        self.theme = ThemeManager()
        self._on_unlock = on_unlock
        self._attempts = 0

        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"{screen_w}x{screen_h}+0+0")
        self.configure(fg_color="#050810")

        self._build_ui(screen_w, screen_h)
        self._tick_clock()

    # ------------------------------------------------------------------ UI
    def _build_ui(self, w, h):
        # Background gradient canvas
        self.canvas = ctk.CTkCanvas(
            self, width=w, height=h,
            highlightthickness=0, bg="#050810"
        )
        self.canvas.place(x=0, y=0)
        self._draw_gradient(w, h)

        # Center container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.45, anchor="center")

        # Clock
        self.time_label = ctk.CTkLabel(
            container, text="00:00",
            font=("Segoe UI", 72, "bold"),
            text_color="#FFFFFF"
        )
        self.time_label.pack(pady=(0, 5))

        # Date
        self.date_label = ctk.CTkLabel(
            container, text="",
            font=("Segoe UI", 18),
            text_color="#888888"
        )
        self.date_label.pack(pady=(0, 40))

        # User avatar
        avatar_frame = ctk.CTkFrame(
            container, width=90, height=90,
            fg_color="#161B22", corner_radius=45,
            border_width=2, border_color="#00E5FF"
        )
        avatar_frame.pack(pady=(0, 12))
        avatar_frame.pack_propagate(False)

        ctk.CTkLabel(
            avatar_frame, text="👤",
            font=("Segoe UI Emoji", 36),
            text_color="#00E5FF"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Username
        ctk.CTkLabel(
            container, text=self.DEFAULT_USERNAME,
            font=("Segoe UI", 18, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(0, 20))

        # Password field
        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter password (default: nova)",
            width=300, height=44,
            show="•",
            fg_color="#161B22",
            text_color="#FFFFFF",
            placeholder_text_color="#555555",
            corner_radius=22,
            border_width=1,
            border_color="#333333",
            font=("Segoe UI", 14)
        )
        self.password_entry.pack(pady=(0, 12))
        self.password_entry.bind("<Return>", lambda e: self._attempt_unlock())
        self.password_entry.focus()

        # Login button
        self.login_btn = ctk.CTkButton(
            container, text="Unlock",
            width=300, height=44,
            fg_color="#00E5FF", text_color="#000000",
            hover_color="#00C8E8",
            corner_radius=22,
            font=("Segoe UI", 15, "bold"),
            command=self._attempt_unlock
        )
        self.login_btn.pack(pady=(0, 8))

        # Error / hint label
        self.hint_label = ctk.CTkLabel(
            container, text="",
            font=("Segoe UI", 12),
            text_color="#FF5252"
        )
        self.hint_label.pack(pady=(0, 0))

        # Version at bottom
        ctk.CTkLabel(
            self, text="NovaOS v0.1.0-alpha",
            font=("Segoe UI", 11),
            text_color="#333333"
        ).place(relx=0.5, rely=0.96, anchor="center")

    # ------------------------------------------------------------------ gradient
    def _draw_gradient(self, w, h):
        steps = 20
        for i in range(steps):
            ratio = i / steps
            r = int(5 + 11 * ratio)
            g = int(8 + 9 * ratio)
            b = int(16 + 5 * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y_start = int(h * i / steps)
            y_end = int(h * (i + 1) / steps)
            self.canvas.create_rectangle(
                0, y_start, w, y_end,
                fill=color, outline=""
            )

    # ------------------------------------------------------------------ clock
    def _tick_clock(self):
        try:
            now = time.time()
            local = time.localtime(now)
            self.time_label.configure(text=time.strftime("%H:%M", local))
            self.date_label.configure(text=time.strftime("%A, %B %d, %Y", local))
            self.after(1000, self._tick_clock)
        except Exception:
            pass

    # ------------------------------------------------------------------ auth
    def _attempt_unlock(self):
        password = self.password_entry.get().strip()

        if password == self.DEFAULT_PASSWORD:
            sound_manager.play("unlock")
            self._unlock()
        else:
            self._attempts += 1
            remaining = 3 - self._attempts
            if remaining > 0:
                sound_manager.play("error")
                self.hint_label.configure(
                    text=f"Wrong password. {remaining} attempts left."
                )
                self.password_entry.delete(0, "end")
                self._shake()
            else:
                self.hint_label.configure(
                    text="Too many failed attempts. Try again in 30s."
                )
                self.login_btn.configure(state="disabled")
                self.after(30000, self._reset_attempts)

    def _reset_attempts(self):
        self._attempts = 0
        self.hint_label.configure(text="")
        self.login_btn.configure(state="normal")

    def _shake(self):
        """Shake the password field to indicate wrong password."""
        original_x = self.password_entry.winfo_x()
        offsets = [8, -8, 6, -6, 3, -3, 0]

        def step(i):
            if i >= len(offsets):
                return
            self.password_entry.place(x=original_x + offsets[i])
            self.after(50, lambda: step(i + 1))

        step(0)

    # ------------------------------------------------------------------ unlock
    def _unlock(self):
        """Fade out and unlock."""
        self._fade_out(8)

    def _fade_out(self, steps):
        if steps <= 0:
            try:
                self.attributes("-alpha", 0.0)
                self.destroy()
            except Exception:
                pass
            if self._on_unlock:
                self._on_unlock()
            return

        try:
            self.attributes("-alpha", steps / 8)
        except Exception:
            pass
        try:
            self.after(30, lambda: self._fade_out(steps - 1))
        except Exception:
            pass
