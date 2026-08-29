"""NovaOS System Monitor application."""

import time
import threading

import psutil
import customtkinter as ctk
from sdk.app import NovaApp
from core.theme import ThemeManager


class SystemMonitorApp(NovaApp):
    """Real-time system monitor with live CPU, RAM, disk, and network stats."""

    APP_NAME = "System Monitor"
    APP_ICON = "📊"
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 580

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self._running = True
        self._cpu_history = [0.0] * 60

    def build(self):
        header = ctk.CTkLabel(
            self.content,
            text="📊  System Monitor",
            font=("Segoe UI", 20, "bold"),
            text_color="#00E5FF"
        )
        header.pack(anchor="w", padx=20, pady=(15, 10))

        # ---------- CPU ----------
        cpu_frame = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=12)
        cpu_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.cpu_title = ctk.CTkLabel(
            cpu_frame, text="CPU", font=("Segoe UI", 14, "bold"),
            text_color="#FFFFFF"
        )
        self.cpu_title.pack(anchor="w", padx=15, pady=(10, 2))

        self.cpu_pct = ctk.CTkLabel(
            cpu_frame, text="0%", font=("Segoe UI", 28, "bold"),
            text_color="#00E5FF"
        )
        self.cpu_pct.pack(anchor="w", padx=15)

        self.cpu_bar_bg = ctk.CTkFrame(cpu_frame, height=10, fg_color="#0D1117", corner_radius=5)
        self.cpu_bar_bg.pack(fill="x", padx=15, pady=(4, 4))
        self.cpu_bar_bg.pack_propagate(False)

        self.cpu_bar = ctk.CTkFrame(self.cpu_bar_bg, height=10, fg_color="#00E5FF", corner_radius=5)
        self.cpu_bar.place(x=0, y=0, relheight=1.0, relwidth=0.0)

        self.cpu_detail = ctk.CTkLabel(
            cpu_frame, text="Cores: — | Frequency: —",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.cpu_detail.pack(anchor="w", padx=15, pady=(2, 10))

        # ---------- CPU History Canvas (use tkinter Canvas, not CTkCanvas) ----------
        import tkinter as tk
        self.cpu_canvas = tk.Canvas(
            cpu_frame, height=60, highlightthickness=0,
            bg="#0D1117"
        )
        self.cpu_canvas.pack(fill="x", padx=15, pady=(0, 10))

        # ---------- RAM ----------
        ram_frame = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=12)
        ram_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.ram_title = ctk.CTkLabel(
            ram_frame, text="Memory (RAM)", font=("Segoe UI", 14, "bold"),
            text_color="#FFFFFF"
        )
        self.ram_title.pack(anchor="w", padx=15, pady=(10, 2))

        self.ram_pct = ctk.CTkLabel(
            ram_frame, text="0%", font=("Segoe UI", 28, "bold"),
            text_color="#FF9800"
        )
        self.ram_pct.pack(anchor="w", padx=15)

        self.ram_bar_bg = ctk.CTkFrame(ram_frame, height=10, fg_color="#0D1117", corner_radius=5)
        self.ram_bar_bg.pack(fill="x", padx=15, pady=(4, 4))
        self.ram_bar_bg.pack_propagate(False)

        self.ram_bar = ctk.CTkFrame(self.ram_bar_bg, height=10, fg_color="#FF9800", corner_radius=5)
        self.ram_bar.place(x=0, y=0, relheight=1.0, relwidth=0.0)

        self.ram_detail = ctk.CTkLabel(
            ram_frame, text="Used: — | Total: —",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.ram_detail.pack(anchor="w", padx=15, pady=(2, 10))

        # ---------- Disk ----------
        disk_frame = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=12)
        disk_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.disk_title = ctk.CTkLabel(
            disk_frame, text="Disk", font=("Segoe UI", 14, "bold"),
            text_color="#FFFFFF"
        )
        self.disk_title.pack(anchor="w", padx=15, pady=(10, 2))

        self.disk_pct = ctk.CTkLabel(
            disk_frame, text="0%", font=("Segoe UI", 28, "bold"),
            text_color="#4CAF50"
        )
        self.disk_pct.pack(anchor="w", padx=15)

        self.disk_bar_bg = ctk.CTkFrame(disk_frame, height=10, fg_color="#0D1117", corner_radius=5)
        self.disk_bar_bg.pack(fill="x", padx=15, pady=(4, 4))
        self.disk_bar_bg.pack_propagate(False)

        self.disk_bar = ctk.CTkFrame(self.disk_bar_bg, height=10, fg_color="#4CAF50", corner_radius=5)
        self.disk_bar.place(x=0, y=0, relheight=1.0, relwidth=0.0)

        self.disk_detail = ctk.CTkLabel(
            disk_frame, text="Used: — | Total: —",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.disk_detail.pack(anchor="w", padx=15, pady=(2, 10))

        # ---------- Network ----------
        net_frame = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=12)
        net_frame.pack(fill="x", padx=20, pady=(0, 8))

        net_header = ctk.CTkFrame(net_frame, fg_color="transparent")
        net_header.pack(fill="x", padx=15, pady=(10, 4))

        ctk.CTkLabel(
            net_header, text="Network", font=("Segoe UI", 14, "bold"),
            text_color="#FFFFFF"
        ).pack(side="left")

        self.net_sent = ctk.CTkLabel(
            net_header, text="↑ 0 B/s",
            font=("Segoe UI", 12), text_color="#2196F3"
        )
        self.net_sent.pack(side="right", padx=(8, 0))

        self.net_recv = ctk.CTkLabel(
            net_header, text="↓ 0 B/s",
            font=("Segoe UI", 12), text_color="#4CAF50"
        )
        self.net_recv.pack(side="right")

        self.net_detail = ctk.CTkLabel(
            net_frame, text="Interfaces: —",
            font=("Segoe UI", 11), text_color="#888888"
        )
        self.net_detail.pack(anchor="w", padx=15, pady=(2, 10))

        # ---------- Processes ----------
        proc_frame = ctk.CTkFrame(self.content, fg_color="#161B22", corner_radius=12)
        proc_frame.pack(fill="x", padx=20, pady=(0, 12))

        self.proc_label = ctk.CTkLabel(
            proc_frame, text="Processes: — | Threads: — | Uptime: —",
            font=("Segoe UI", 12), text_color="#BBBBBB"
        )
        self.proc_label.pack(anchor="w", padx=15, pady=10)

        # Start live updates in background thread
        self._prev_net = psutil.net_io_counters()
        self._start_updater()

    # -------------------------------------------------------------- updater
    def _start_updater(self):
        def loop():
            if not self._running:
                return
            try:
                self._update_stats()
            except Exception as e:
                print(f"[SystemMonitor] update error: {e}")
            if self._running:
                self.after(1000, loop)

        self.after(500, loop)

    def _update_stats(self):
        # CPU
        cpu = psutil.cpu_percent(interval=0)
        self._cpu_history.append(cpu)
        if len(self._cpu_history) > 60:
            self._cpu_history.pop(0)

        self.cpu_pct.configure(text=f"{cpu:.1f}%")
        color = "#FF5252" if cpu > 80 else "#FF9800" if cpu > 50 else "#00E5FF"
        self.cpu_bar.place_configure(relwidth=cpu / 100)
        self.cpu_bar.configure(fg_color=color)
        self.cpu_pct.configure(text_color=color)

        freq = psutil.cpu_freq()
        freq_str = f"{freq.current:.0f} MHz" if freq else "N/A"
        cores = psutil.cpu_count(logical=True)
        self.cpu_detail.configure(text=f"Cores: {cores} | Frequency: {freq_str}")

        # CPU history graph
        self._draw_cpu_history()

        # RAM
        ram = psutil.virtual_memory()
        self.ram_pct.configure(text=f"{ram.percent:.1f}%")
        self.ram_bar.place_configure(relwidth=ram.percent / 100)
        used_gb = ram.used / (1024 ** 3)
        total_gb = ram.total / (1024 ** 3)
        self.ram_detail.configure(
            text=f"Used: {used_gb:.1f} GB | Total: {total_gb:.1f} GB"
        )

        # Disk
        try:
            disk = psutil.disk_usage("/")
        except Exception:
            disk = psutil.disk_usage("C:\\")
        self.disk_pct.configure(text=f"{disk.percent:.1f}%")
        self.disk_bar.place_configure(relwidth=disk.percent / 100)
        d_used = disk.used / (1024 ** 3)
        d_total = disk.total / (1024 ** 3)
        self.disk_detail.configure(
            text=f"Used: {d_used:.1f} GB | Total: {d_total:.1f} GB"
        )

        # Network
        net = psutil.net_io_counters()
        dt = 1.0
        sent_speed = (net.bytes_sent - self._prev_net.bytes_sent) / dt
        recv_speed = (net.bytes_recv - self._prev_net.bytes_recv) / dt
        self._prev_net = net

        self.net_sent.configure(text=f"↑ {self._format_speed(sent_speed)}")
        self.net_recv.configure(text=f"↓ {self._format_speed(recv_speed)}")

        interfaces = len(psutil.net_if_stats())
        self.net_detail.configure(text=f"Interfaces: {interfaces}")

        # Processes
        proc_count = len(psutil.pids())
        import platform
        uptime_s = time.time() - psutil.boot_time()
        days = int(uptime_s // 86400)
        hours = int((uptime_s % 86400) // 3600)
        mins = int((uptime_s % 3600) // 60)
        uptime_str = f"{days}d {hours}h {mins}m" if days else f"{hours}h {mins}m"
        self.proc_label.configure(
            text=f"Processes: {proc_count} | Uptime: {uptime_str}"
        )

    # -------------------------------------------------------------- helpers
    def _format_speed(self, bps):
        """Format bytes per second to human-readable string."""
        if bps < 1024:
            return f"{bps:.0f} B/s"
        elif bps < 1024 ** 2:
            return f"{bps / 1024:.1f} KB/s"
        elif bps < 1024 ** 3:
            return f"{bps / (1024 ** 2):.1f} MB/s"
        else:
            return f"{bps / (1024 ** 3):.2f} GB/s"

    def _draw_cpu_history(self):
        """Draw CPU usage history as a line graph on canvas."""
        try:
            self.cpu_canvas.delete("all")
        except Exception:
            return

        try:
            w = self.cpu_canvas.winfo_width()
            h = self.cpu_canvas.winfo_height()
        except Exception:
            return

        if w < 10 or h < 10:
            return

        data = self._cpu_history
        n = len(data)
        if n < 2:
            return

        step = w / (n - 1)
        points = []
        for i, val in enumerate(data):
            x = i * step
            y = h - (val / 100.0) * (h - 4) - 2
            points.append((x, y))

        # Draw filled area
        fill_coords = [(0, h)] + points + [(w, h)]
        flat = [c for p in fill_coords for c in p]
        self.cpu_canvas.create_polygon(
            flat, fill="#0D2833", outline=""
        )

        # Draw line
        flat_line = [c for p in points for c in p]
        if len(flat_line) >= 4:
            self.cpu_canvas.create_line(
                flat_line, fill="#00E5FF", width=2, smooth=True
            )

    # -------------------------------------------------------------- cleanup
    def destroy(self):
        self._running = False
        super().destroy()
