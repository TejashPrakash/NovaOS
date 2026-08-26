"""Animated boot splash screen for NovaOS."""

import customtkinter as ctk
import math
from core.theme import ThemeManager
from core.sounds import sound_manager


class NovaSplashScreen(ctk.CTkToplevel):
    """Full-screen animated boot splash that runs before the desktop."""

    BOOT_MESSAGES = [
        "Initializing NovaOS kernel...",
        "Loading core services...",
        "Starting AI subsystem...",
        "Mounting virtual filesystem...",
        "Loading desktop environment...",
        "Initializing window manager...",
        "Loading AI skills...",
        "Starting voice provider...",
        "Loading user preferences...",
        "Applying cyberpunk theme...",
        "Starting process manager...",
        "Booting NovaOS..."
    ]

    def __init__(self):
        super().__init__()

        self.theme = ThemeManager()
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.overrideredirect(True)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"{screen_w}x{screen_h}+0+0")
        self.configure(fg_color="#050810")

        self._animation_step = 0
        self._particles = []
        self._message_index = 0
        self._progress = 0.0
        self._boot_complete = False
        self._on_complete = None

        self._build_ui()
        self._init_particles(screen_w, screen_h)

    def _build_ui(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.bg_canvas = ctk.CTkCanvas(
            self,
            width=self.winfo_screenwidth(),
            height=self.winfo_screenheight(),
            highlightthickness=0,
            bg="#050810"
        )
        self.bg_canvas.place(x=0, y=0)

        self.logo_label = ctk.CTkLabel(
            self.container, text="◈",
            font=("Segoe UI Emoji", 96),
            text_color="#00E5FF"
        )
        self.logo_label.pack(pady=(0, 10))

        self.title_label = ctk.CTkLabel(
            self.container, text="NovaOS",
            font=("Segoe UI", 48, "bold"),
            text_color="#00E5FF"
        )
        self.title_label.pack(pady=(0, 5))

        self.subtitle_label = ctk.CTkLabel(
            self.container,
            text="AI-Powered Desktop Operating System",
            font=("Segoe UI", 16),
            text_color="#666666"
        )
        self.subtitle_label.pack(pady=(0, 50))

        self.progress_bg = ctk.CTkFrame(
            self.container, width=400, height=6,
            fg_color="#161B22", corner_radius=3
        )
        self.progress_bg.pack(pady=(0, 15))
        self.progress_bg.pack_propagate(False)

        self.progress_fill = ctk.CTkFrame(
            self.progress_bg, width=0, height=6,
            fg_color="#00E5FF", corner_radius=3
        )
        self.progress_fill.place(x=0, y=0, relheight=1.0)

        self.status_label = ctk.CTkLabel(
            self.container, text="",
            font=("Segoe UI", 12), text_color="#888888"
        )
        self.status_label.pack(pady=(5, 0))

        self.version_label = ctk.CTkLabel(
            self, text="v0.1.0-alpha",
            font=("Segoe UI", 11), text_color="#333333"
        )
        self.version_label.place(relx=0.5, rely=0.95, anchor="center")

    def _init_particles(self, w, h):
        import random
        self._particles = []
        for _ in range(40):
            self._particles.append({
                "x": random.uniform(0, w),
                "y": random.uniform(0, h),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.5, -0.1),
                "size": random.randint(1, 3),
                "brightness": random.randint(40, 120),
            })

    def _draw_particles(self):
        self.bg_canvas.delete("particles")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -10:
                p["y"] = h + 10
                p["x"] = p["x"] % w
            if p["x"] < -10:
                p["x"] = w + 10
            elif p["x"] > w + 10:
                p["x"] = -10
            b = p["brightness"]
            color = f"#{b:02x}{int(b*0.9):02x}{int(b*1.15):02x}"
            self.bg_canvas.create_oval(
                p["x"], p["y"], p["x"] + p["size"], p["y"] + p["size"],
                fill=color, outline="", tags="particles"
            )

    def _animate(self):
        if self._boot_complete:
            return
        self._animation_step += 1
        self._draw_particles()

        pulse = 0.7 + 0.3 * math.sin(self._animation_step * 0.08)
        glow_b = int(229 * pulse)
        self.logo_label.configure(
            text_color=f"#{glow_b:02x}{int(glow_b*0.97):02x}ff"
        )

        if self._progress < 1.0:
            speed = 0.008 + (self._progress * 0.015)
            self._progress = min(1.0, self._progress + speed)
            self.progress_fill.configure(width=int(400 * self._progress))
            msg_idx = min(
                int(self._progress * len(self.BOOT_MESSAGES)),
                len(self.BOOT_MESSAGES) - 1
            )
            if msg_idx != self._message_index:
                self._message_index = msg_idx
                self.status_label.configure(text=self.BOOT_MESSAGES[msg_idx])

        if self._progress >= 1.0 and not self._boot_complete:
            self._boot_complete = True
            self.status_label.configure(text="NovaOS Ready")
            self.after(400, self._finish_boot)
            return

        self.after(30, self._animate)

    def start_boot(self, callback):
        self._on_complete = callback
        self._animate()

    def _finish_boot(self):
        self._boot_complete = True
        sound_manager.play("boot")
        self._fade_out(10)

    def _fade_out(self, steps):
        if steps <= 0:
            if self._on_complete:
                self._on_complete()
            try:
                self.place_forget()
                self.destroy()
            except Exception:
                pass
            return

        alpha = steps / 10
        bg = f"#{int(5*alpha):02x}{int(8*alpha):02x}{int(16*alpha):02x}"
        try:
            self.configure(fg_color=bg)
            self.bg_canvas.configure(bg=bg)
        except Exception:
            pass

        for child in self.container.winfo_children():
            try:
                child.configure(text_color=bg)
            except Exception:
                pass
        try:
            self.after(40, lambda: self._fade_out(steps - 1))
        except Exception:
            pass