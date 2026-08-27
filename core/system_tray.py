"""System tray for NovaOS — clock, volume, network, CPU, and quick settings."""

import time
import psutil
import customtkinter as ctk
from core.theme import ThemeManager


class SystemTray(ctk.CTkFrame):
    """Bottom-right system tray with live indicators and quick settings."""

    def __init__(self, master, kernel=None, **kwargs):
        super().__init__(
            master,
            fg_color="#0D1117",
            corner_radius=12,
            border_width=1,
            border_color="#222222",
            **kwargs
        )
        self.kernel = kernel
        self.theme = ThemeManager()
        self._settings_open = False
        self._settings_panel = None

        self._build_ui()
        self._tick()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        # ---- Clock ----
        self.clock_label = ctk.CTkLabel(
            self, text="00:00",
            font=("Segoe UI", 13, "bold"),
            text_color="#FFFFFF"
        )
        self.clock_label.pack(side="left", padx=(12, 6), pady=8)

        # Separator
        sep1 = ctk.CTkLabel(self, text="│", text_color="#333333", font=("Segoe UI", 13))
        sep1.pack(side="left", padx=2)

        # ---- CPU mini indicator ----
        self.cpu_label = ctk.CTkLabel(
            self, text="⚡ --",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.cpu_label.pack(side="left", padx=6, pady=8)

        # ---- RAM mini indicator ----
        self.ram_label = ctk.CTkLabel(
            self, text="💾 --",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.ram_label.pack(side="left", padx=6, pady=8)

        # ---- Network indicator ----
        self.net_label = ctk.CTkLabel(
            self, text="🌐 --",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.net_label.pack(side="left", padx=6, pady=8)

        # Separator
        sep2 = ctk.CTkLabel(self, text="│", text_color="#333333", font=("Segoe UI", 13))
        sep2.pack(side="left", padx=2)

        # ---- Quick settings button ----
        self.settings_btn = ctk.CTkButton(
            self, text="⚙", width=30, height=28,
            fg_color="transparent", text_color="#888888",
            hover_color="#1C2333", corner_radius=6,
            font=("Segoe UI", 14),
            command=self._toggle_settings
        )
        self.settings_btn.pack(side="right", padx=(0, 8), pady=6)

        # ---- Volume icon ----
        self.vol_label = ctk.CTkLabel(
            self, text="🔊",
            font=("Segoe UI Emoji", 13), text_color="#888888"
        )
        self.vol_label.pack(side="right", padx=4, pady=8)

    # ------------------------------------------------------------------ live updates
    def _tick(self):
        try:
            now = time.localtime()
            self.clock_label.configure(text=time.strftime("%H:%M", now))

            cpu = psutil.cpu_percent(interval=0)
            cpu_color = "#FF5252" if cpu > 80 else "#FF9800" if cpu > 50 else "#4CAF50"
            self.cpu_label.configure(text=f"⚡ {cpu:.0f}%", text_color=cpu_color)

            ram = psutil.virtual_memory()
            ram_color = "#FF5252" if ram.percent > 80 else "#FF9800" if ram.percent > 50 else "#00E5FF"
            self.ram_label.configure(text=f"💾 {ram.percent:.0f}%", text_color=ram_color)

            # Network status
            try:
                stats = psutil.net_if_stats()
                up = any(s.isup for s in stats.values())
                self.net_label.configure(
                    text="🌐 Online" if up else "🌐 Offline",
                    text_color="#4CAF50" if up else "#FF5252"
                )
            except Exception:
                self.net_label.configure(text="🌐 --", text_color="#888888")

        except Exception:
            pass

        self.after(2000, self._tick)

    # ------------------------------------------------------------------ quick settings
    def _toggle_settings(self):
        if self._settings_open:
            self._close_settings()
            return

        self._settings_open = True

        # Create on ROOT, not self — prevents ghost dark space on destroy
        root = self.winfo_toplevel()
        self._settings_panel = ctk.CTkToplevel(root)
        self._settings_panel.title("")
        self._settings_panel.geometry("280x320")
        self._settings_panel.configure(fg_color="#0D1117")
        self._settings_panel.overrideredirect(True)
        self._settings_panel.attributes("-topmost", True)
        self._settings_panel.transient(root)

        # Position above tray
        x = self.winfo_rootx() + self.winfo_width() - 280
        y = self.winfo_rooty() - 330
        self._settings_panel.geometry(f"+{x}+{y}")

        # Close when clicking outside (use root bind to catch all clicks)
        def _on_root_click(e):
            # Ignore clicks inside the panel
            try:
                px = self._settings_panel.winfo_rootx()
                py = self._settings_panel.winfo_rooty()
                pw = self._settings_panel.winfo_width()
                ph = self._settings_panel.winfo_height()
                if px <= e.x_root <= px + pw and py <= e.y_root <= py + ph:
                    return
            except Exception:
                pass
            self._close_settings()

        root.bind("<Button-1>", _on_root_click, add="+")
        self._root_click_handler = _on_root_click

        # ---- Theme selector ----
        ctk.CTkLabel(
            self._settings_panel, text="Quick Settings",
            font=("Segoe UI", 14, "bold"), text_color="#FFFFFF"
        ).pack(pady=(12, 8))

        # Theme row
        theme_frame = ctk.CTkFrame(self._settings_panel, fg_color="transparent")
        theme_frame.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(
            theme_frame, text="🎨 Theme", font=("Segoe UI", 12),
            text_color="#BBBBBB"
        ).pack(side="left")

        theme_names = ["cyberpunk", "midnight", "ocean", "forest", "sunset", "arctic"]
        self.theme_var = ctk.StringVar(value=self.theme.get_current_theme() if hasattr(self.theme, 'get_current_theme') else "cyberpunk")

        for name in theme_names:
            btn = ctk.CTkRadioButton(
                theme_frame, text=name.title(), variable=self.theme_var,
                value=name, fg_color="#00E5FF", text_color="#888888",
                hover_color="#00C8E8", border_color="#555555",
                font=("Segoe UI", 11),
                command=self._apply_theme
            )
            btn.pack(anchor="w", padx=(10, 0), pady=1)

        # Separator
        ctk.CTkFrame(self._settings_panel, height=1, fg_color="#333333").pack(
            fill="x", padx=15, pady=8
        )

        # Volume row
        vol_frame = ctk.CTkFrame(self._settings_panel, fg_color="transparent")
        vol_frame.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(
            vol_frame, text="🔊 Volume", font=("Segoe UI", 12),
            text_color="#BBBBBB"
        ).pack(side="left")

        vol_slider = ctk.CTkSlider(
            vol_frame, from_=0, to=1, width=120, height=12,
            button_color="#00E5FF", progress_color="#00E5FF",
            fg_color="#333333", command=self._on_volume
        )
        vol_slider.pack(side="right")
        vol_slider.set(0.7)

        # Separator
        ctk.CTkFrame(self._settings_panel, height=1, fg_color="#333333").pack(
            fill="x", padx=15, pady=8
        )

        # Premium effects toggle
        effects_frame = ctk.CTkFrame(self._settings_panel, fg_color="transparent")
        effects_frame.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(
            effects_frame, text="✨ Effects", font=("Segoe UI", 12),
            text_color="#BBBBBB"
        ).pack(side="left")

        self.effects_switch = ctk.CTkSwitch(
            effects_frame, text="",
            progress_color="#00E5FF",
            button_color="#FFFFFF",
            button_hover_color="#00C8E8",
            command=self._toggle_effects
        )
        self.effects_switch.pack(side="right")

        # Separator
        ctk.CTkFrame(self._settings_panel, height=1, fg_color="#333333").pack(
            fill="x", padx=15, pady=8
        )

        # Lock screen
        lock_btn = ctk.CTkButton(
            self._settings_panel, text="🔒 Lock Screen",
            height=34, corner_radius=8,
            fg_color="#161B22", text_color="#FFFFFF",
            hover_color="#1C2333", border_width=1, border_color="#333333",
            font=("Segoe UI", 12),
            command=self._lock_screen
        )
        lock_btn.pack(fill="x", padx=15, pady=4)

        self._settings_panel.focus_set()

    def _close_settings(self):
        self._settings_open = False
        if self._settings_panel:
            try:
                root = self.winfo_toplevel()
                if hasattr(self, '_root_click_handler'):
                    root.unbind("<Button-1>", self._root_click_handler)
            except Exception:
                pass
            try:
                self._settings_panel.destroy()
            except Exception:
                pass
            self._settings_panel = None
            # Force root to repaint — clears ghost dark space
            try:
                self.winfo_toplevel().update_idletasks()
            except Exception:
                pass

    def _apply_theme(self):
        theme_name = self.theme_var.get()
        if self.kernel and hasattr(self.kernel, 'set_theme'):
            self.kernel.set_theme(theme_name)

    def _on_volume(self, value):
        if self.kernel:
            audio = self.kernel.get_service("audio")
            if audio:
                audio.set_volume(value)

    def _toggle_effects(self):
        enabled = self.effects_switch.get()
        if self.kernel and hasattr(self.kernel, 'desktop'):
            desktop = self.kernel.desktop
            if enabled:
                desktop.enable_neural_network_background()
                desktop.enable_ambient_lighting()
            else:
                desktop.disable_neural_network_background()
                desktop.disable_ambient_lighting()

    def _lock_screen(self):
        self._close_settings()
        from core.lock_screen import LockScreen
        LockScreen(on_unlock=lambda: None)
