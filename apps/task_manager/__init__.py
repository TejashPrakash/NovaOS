"""NovaOS Task Manager — view and manage running processes."""

import time
import threading
import psutil
import customtkinter as ctk
from sdk.app import NovaApp


class TaskManagerApp(NovaApp):
    APP_NAME = "Task Manager"
    APP_ICON = "📋"
    DEFAULT_WIDTH = 750
    DEFAULT_HEIGHT = 550

    def __init__(self, window):
        super().__init__(window)
        self._running = True
        self._selected_pid = None

    def build(self):
        # Header
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(12, 8))

        ctk.CTkLabel(header, text="📋  Task Manager",
            font=("Segoe UI", 20, "bold"), text_color="#00E5FF"
        ).pack(side="left")

        # Refresh rate selector
        ctk.CTkLabel(header, text="Refresh:", font=("Segoe UI", 11), text_color="#888888").pack(side="right")
        self.refresh_var = ctk.StringVar(value="2s")
        ctk.CTkComboBox(header, values=["1s", "2s", "5s"], variable=self.refresh_var,
            width=60, height=28, fg_color="#161B22", text_color="#FFFFFF",
            button_color="#00E5FF", dropdown_fg_color="#161B22", corner_radius=6
        ).pack(side="right", padx=(5, 10))

        # Summary cards
        self._build_summary()

        # Process table
        self._build_table()

        # Action buttons
        self._build_actions()

        # Start live updates
        self._tick()

    def _build_summary(self):
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(0, 8))

        self.cpu_card = self._stat_card(frame, "⚡ CPU", "0%", "#00E5FF")
        self.cpu_card.pack(side="left", padx=(0, 8), expand=True, fill="x")

        self.mem_card = self._stat_card(frame, "💾 RAM", "0%", "#7B61FF")
        self.mem_card.pack(side="left", padx=(0, 8), expand=True, fill="x")

        self.disk_card = self._stat_card(frame, "💿 Disk", "0%", "#FF9800")
        self.disk_card.pack(side="left", padx=(0, 8), expand=True, fill="x")

        self.proc_card = self._stat_card(frame, "⚙ Processes", "0", "#4CAF50")
        self.proc_card.pack(side="left", expand=True, fill="x")

    def _stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color="#161B22", corner_radius=10, height=70)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 11), text_color="#888888").pack(pady=(10, 0))
        label = ctk.CTkLabel(card, text=value, font=("Segoe UI", 18, "bold"), text_color=color)
        label.pack()
        card._value_label = label
        return card

    def _build_table(self):
        # Table header
        cols_frame = ctk.CTkFrame(self.content, fg_color="#1A1F2B", corner_radius=8, height=35)
        cols_frame.pack(fill="x", padx=15)
        cols_frame.pack_propagate(False)

        headers = [("PID", 80), ("Name", 250), ("CPU%", 80), ("MEM%", 80), ("Status", 80), ("Threads", 80)]
        for text, width in headers:
            ctk.CTkLabel(cols_frame, text=text, width=width,
                font=("Segoe UI", 11, "bold"), text_color="#00E5FF"
            ).pack(side="left", padx=2, pady=6)

        # Scrollable process list
        self.process_frame = ctk.CTkScrollableFrame(self.content, fg_color="#0D1117", corner_radius=8)
        self.process_frame.pack(fill="both", expand=True, padx=15, pady=(4, 8))

        self.process_rows = []

    def _build_actions(self):
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(0, 10))

        btn_style = dict(height=32, corner_radius=8, font=("Segoe UI", 11, "bold"))

        ctk.CTkButton(frame, text="🔍 Search", fg_color="#161B22", text_color="#00E5FF",
            hover_color="#1C2333", border_width=1, border_color="#333333",
            command=self._search_process, **btn_style
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(frame, text="🔄 End Task", fg_color="#E53935", text_color="white",
            hover_color="#C62828", command=self._end_task, **btn_style
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(frame, text="⏸ Suspend", fg_color="#FF9800", text_color="black",
            hover_color="#F57C00", command=self._suspend_task, **btn_style
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(frame, text="▶ Resume", fg_color="#4CAF50", text_color="white",
            hover_color="#388E3C", command=self._resume_task, **btn_style
        ).pack(side="left")

        # Status
        self.status_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 10), text_color="#888888")
        self.status_label.pack(side="right")

    def _tick(self):
        if not self._running:
            return
        try:
            # Update summary cards
            cpu = psutil.cpu_percent(interval=0)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            procs = len(psutil.pids())

            self.cpu_card._value_label.configure(text=f"{cpu:.1f}%")
            self.mem_card._value_label.configure(text=f"{mem.percent:.1f}%")
            self.disk_card._value_label.configure(text=f"{disk.percent:.1f}%")
            self.proc_card._value_label.configure(text=str(procs))

            # Update process list
            self._refresh_processes()
        except Exception:
            pass

        # Schedule next tick
        rate = self.refresh_var.get()
        ms = {"1s": 1000, "2s": 2000, "5s": 5000}.get(rate, 2000)
        self.after(ms, self._tick)

    def _refresh_processes(self):
        # Clear old rows
        for row in self.process_rows:
            row.destroy()
        self.process_rows.clear()

        # Get all processes sorted by CPU
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "num_threads"]):
            try:
                info = p.info
                procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        procs.sort(key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)

        for info in procs[:50]:  # Show top 50
            pid = info.get("pid", 0)
            name = info.get("name", "?")[:30]
            cpu = info.get("cpu_percent", 0) or 0
            mem = info.get("memory_percent", 0) or 0
            status = info.get("status", "?")
            threads = info.get("num_threads", 0)

            bg = "#161B22" if len(self.process_rows) % 2 == 0 else "#0D1117"

            row = ctk.CTkFrame(self.process_frame, fg_color=bg, corner_radius=4, height=30)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            # Color code CPU
            cpu_color = "#FF5252" if cpu > 50 else "#FF9800" if cpu > 20 else "#4CAF50" if cpu > 0 else "#888888"
            mem_color = "#FF5252" if mem > 20 else "#FF9800" if mem > 10 else "#00E5FF"

            cols = [
                (str(pid), 80, "#BBBBBB"),
                (name, 250, "#FFFFFF"),
                (f"{cpu:.1f}", 80, cpu_color),
                (f"{mem:.1f}", 80, mem_color),
                (status, 80, "#4CAF50" if status == "running" else "#FFC107"),
                (str(threads), 80, "#888888"),
            ]

            for text, width, color in cols:
                ctk.CTkLabel(row, text=text, width=width, font=("Segoe UI", 10),
                    text_color=color, anchor="w"
                ).pack(side="left", padx=2, pady=4)

            # Click to select
            row.bind("<Button-1>", lambda e, p=pid, r=row: self._select_row(p, r))
            self.process_rows.append(row)

    def _select_row(self, pid, row):
        self._selected_pid = pid
        # Highlight
        for r in self.process_rows:
            r.configure(fg_color="#0D1117")
        row.configure(fg_color="#003344")

    def _end_task(self):
        if not self._selected_pid:
            self.status_label.configure(text="⚠ Select a process first", text_color="#FFC107")
            return
        try:
            p = psutil.Process(self._selected_pid)
            p.terminate()
            self.status_label.configure(text=f"✅ Terminated PID {self._selected_pid}", text_color="#4CAF50")
            self._selected_pid = None
        except psutil.NoSuchProcess:
            self.status_label.configure(text="❌ Process already gone", text_color="#E53935")
        except psutil.AccessDenied:
            self.status_label.configure(text="❌ Access denied", text_color="#E53935")

    def _suspend_task(self):
        if not self._selected_pid:
            self.status_label.configure(text="⚠ Select a process first", text_color="#FFC107")
            return
        try:
            p = psutil.Process(self._selected_pid)
            p.suspend()
            self.status_label.configure(text=f"⏸ Suspended PID {self._selected_pid}", text_color="#FF9800")
        except Exception as e:
            self.status_label.configure(text=f"❌ {e}", text_color="#E53935")

    def _resume_task(self):
        if not self._selected_pid:
            self.status_label.configure(text="⚠ Select a process first", text_color="#FFC107")
            return
        try:
            p = psutil.Process(self._selected_pid)
            p.resume()
            self.status_label.configure(text=f"▶ Resumed PID {self._selected_pid}", text_color="#4CAF50")
        except Exception as e:
            self.status_label.configure(text=f"❌ {e}", text_color="#E53935")

    def _search_process(self):
        """Show search dialog."""
        root = self.content.winfo_toplevel()
        dialog = ctk.CTkToplevel(root)
        dialog.title("Search Process")
        dialog.geometry("350x120")
        dialog.configure(fg_color="#0D1117")
        dialog.attributes("-topmost", True)
        dialog.transient(root)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Search by name:", font=("Segoe UI", 12), text_color="#BBBBBB").pack(pady=(12, 4))
        entry = ctk.CTkEntry(dialog, width=280, height=32, fg_color="#161B22", text_color="#FFFFFF", corner_radius=8)
        entry.pack(pady=4)
        entry.focus()

        def do_search():
            query = entry.get().strip().lower()
            if not query:
                return
            # Highlight matching processes
            for row in self.process_rows:
                name_text = ""
                for child in row.winfo_children():
                    if isinstance(child, ctk.CTkLabel):
                        name_text = child.cget("text")
                        break
                if query in name_text.lower():
                    row.configure(fg_color="#003344")
                else:
                    row.configure(fg_color="#0D1117")
            dialog.destroy()

        entry.bind("<Return>", lambda e: do_search())

    def destroy(self):
        self._running = False
        super().destroy()
