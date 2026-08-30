"""Animated boot splash screen for NovaOS."""

import random
import math
import customtkinter as ctk
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
        "Loading 34 AI skills...",
        "Starting voice provider...",
        "Loading user preferences...",
        "Applying cyberpunk theme...",
        "Starting process manager...",
        "Booting NovaOS..."
    ]

    FEATURES = [
        "🤖 34 AI Skills  •  🌐 Chromium Browser  •  🎨 7 Themes",
        "📁 File Operations  •  🖥 Virtual Desktops  •  🎵 Music Player",
        "📊 System Monitor  •  📋 Task Manager  •  🌤 Weather Live",
        "📝 Smart Notes  •  📅 Calendar Events  •  >_ Terminal 30+ Commands",
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
        self._message_index = 0
        self._progress = 0.0
        self._boot_complete = False
        self._on_complete = None
        self._orb_widgets = []
        self._particle_widgets = []

        self._build_ui()
        self._init_orbs(screen_w, screen_h)

    def _build_ui(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

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
            self, text="v0.1.0-alpha  •  AI-Powered Desktop",
            font=("Segoe UI", 11), text_color="#333333"
        )
        self.version_label.place(relx=0.5, rely=0.95, anchor="center")

        # Feature highlights at bottom
        self.feature_label = ctk.CTkLabel(
            self, text="",
            font=("Segoe UI", 12), text_color="#444444"
        )
        self.feature_label.place(relx=0.5, rely=0.88, anchor="center")
        self._feature_index = 0

    def _init_orbs(self, w, h):
        """Create floating glowing orb frames."""
        orb_colors = ["#00E5FF", "#7B61FF", "#FF00E5", "#00FF88"]
        for _ in range(6):
            color = random.choice(orb_colors)
            size = random.randint(60, 160)
            x = random.randint(0, max(1, w - size))
            y = random.randint(0, max(1, h - size))

            orb = ctk.CTkFrame(
                self, width=size, height=size,
                fg_color=color, corner_radius=size // 2,
            )
            orb.place(x=x, y=y)
            self._orb_widgets.append({
                "widget": orb,
                "x": float(x), "y": float(y),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.3, 0.3),
                "size": size,
            })

        # Small particle dots
        for _ in range(20):
            color = random.choice(orb_colors)
            size = random.randint(2, 6)
            x = random.randint(0, w)
            y = random.randint(0, h)

            dot = ctk.CTkFrame(
                self, width=size, height=size,
                fg_color=color, corner_radius=size // 2,
            )
            dot.place(x=x, y=y)
            self._particle_widgets.append({
                "widget": dot,
                "x": float(x), "y": float(y),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.8, -0.1),
                "size": size,
            })

    def _animate(self):
        if self._boot_complete:
            return
        self._animation_step += 1

        # Pulse logo
        pulse = 0.7 + 0.3 * math.sin(self._animation_step * 0.08)
        glow_b = int(229 * pulse)
        self.logo_label.configure(
            text_color=f"#{min(255, glow_b):02x}{min(255, int(glow_b * 0.97)):02x}ff"
        )

        # Move orbs
        try:
            w = self.winfo_screenwidth()
            h = self.winfo_screenheight()
            for orb_data in self._orb_widgets:
                orb_data["x"] += orb_data["vx"]
                orb_data["y"] += orb_data["vy"]
                ox = orb_data["x"]
                oy = orb_data["y"]
                sz = orb_data["size"]

                if ox < -sz:
                    orb_data["x"] = w
                elif ox > w:
                    orb_data["x"] = -sz
                if oy < -sz:
                    orb_data["y"] = h
                elif oy > h:
                    orb_data["y"] = -sz

                pulse_s = 0.6 + 0.4 * math.sin(self._animation_step * 0.04 + ox * 0.003)
                new_sz = max(20, int(sz * pulse_s))
                orb_data["widget"].place(
                    x=int(orb_data["x"]), y=int(orb_data["y"]),
                    width=new_sz, height=new_sz,
                )

            # Move particles
            for p_data in self._particle_widgets:
                p_data["x"] += p_data["vx"]
                p_data["y"] += p_data["vy"]
                if p_data["y"] < -10:
                    p_data["y"] = h + 10
                    p_data["x"] = random.uniform(0, w)
                if p_data["x"] < -10:
                    p_data["x"] = w + 10
                elif p_data["x"] > w + 10:
                    p_data["x"] = -10
                p_data["widget"].place(
                    x=int(p_data["x"]), y=int(p_data["y"]),
                    width=p_data["size"], height=p_data["size"],
                )
        except Exception:
            pass

        # Cycle feature highlights
        if self._animation_step % 120 == 0 and self.FEATURES:
            self._feature_index = (self._feature_index + 1) % len(self.FEATURES)
            self.feature_label.configure(text=self.FEATURES[self._feature_index])

        # Progress bar
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
        if self.FEATURES:
            self.feature_label.configure(text=self.FEATURES[0])
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
