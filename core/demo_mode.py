"""NovaOS Demo Mode — auto-showcase of all features with narrated transitions.

Launch with Ctrl+D or from the dock. Plays through each major feature
with a narrator overlay explaining what's happening.
"""

import time
import threading
import customtkinter as ctk


class DemoMode(ctk.CTkToplevel):
    """Full-screen demo overlay that walks through NovaOS features."""

    FEATURES = [
        {
            "title": "🖥️  Welcome to NovaOS",
            "desc": "An AI-Powered Desktop Operating System\nbuilt entirely in Python with CustomTkinter.\n\nLet me show you what makes it special.",
            "action": None,
        },
        {
            "title": "🤖  AI Assistant — 34 Skills",
            "desc": "NovaOS has a built-in AI assistant powered by\nGoogle Gemini (cloud) or Ollama (local).\n\nIt can control the entire OS through natural language:\n• Open/close apps  • Change themes\n• Search the web    • Create notes\n• Get weather       • Run calculations",
            "action": "toggle_ai_panel",
        },
        {
            "title": "🌐  Chromium Browser",
            "desc": "A full Chromium browser embedded inside NovaOS\nusing Playwright — no external browser needed.\n\nYouTube, Google, any website works with\nfull JavaScript, CSS, and HTML5 support.",
            "action": "open_browser",
        },
        {
            "title": "📝  Smart Notes with AI",
            "desc": "Create, edit, save, and delete notes.\n\nThe AI Assist button analyzes your notes and\nsuggests improvements in real-time.",
            "action": "open_notes",
        },
        {
            "title": "📁  File Manager with Operations",
            "desc": "Full file management: navigate, copy, cut,\npaste, delete, and rename files.\n\nRight-click any file for a context menu.\nPress Ctrl+C / Ctrl+V for clipboard operations.",
            "action": "open_files",
        },
        {
            "title": ">_  Terminal — 30+ Commands",
            "desc": "A fully functional terminal with:\n• Built-in commands (ls, cd, cat, grep, tree...)\n• Tab completion  • Command history\n• Aliases          • System commands\n• neofetch display",
            "action": "open_terminal",
        },
        {
            "title": "🎵  Music Player",
            "desc": "Play local music files with full controls:\nplay, pause, stop, next, previous, volume.\n\nSupports MP3, WAV, OGG, FLAC, M4A, AAC.\nPlaylist management with auto-advance.",
            "action": "open_music",
        },
        {
            "title": "🌤  Weather Dashboard",
            "desc": "Live weather data from OpenWeatherMap API.\n\nTemperature, humidity, wind, pressure,\nvisibility — all with visual indicators.",
            "action": "open_weather",
        },
        {
            "title": "📊  System Monitor",
            "desc": "Real-time system monitoring:\n• CPU usage with history graph\n• RAM usage and availability\n• Disk usage per partition\n• Network interface status",
            "action": "open_system_monitor",
        },
        {
            "title": "📋  Task Manager",
            "desc": "View and manage all running processes:\n• Sort by CPU/Memory usage\n• Search and filter processes\n• Suspend, resume, or terminate tasks\n• Live updating at configurable intervals",
            "action": "open_task_manager",
        },
        {
            "title": "📅  Calendar & 🧮  Calculator",
            "desc": "Calendar with event management and persistence.\nCalculator with themed buttons and safe evaluation.\n\nBoth with AI integration for smart features.",
            "action": "open_calendar",
        },
        {
            "title": "🎨  7 Premium Themes",
            "desc": "Switch between 7 stunning themes:\nCyberpunk • Midnight • Ocean • Forest\nSunset    • Arctic   • Neon\n\nNeural background and ambient lighting\neffects can be toggled from Settings.",
            "action": "show_themes",
        },
        {
            "title": "🖥️  Virtual Desktops",
            "desc": "4 switchable workspaces for organization.\n\nUse Ctrl+1/2/3/4 to switch between them.\nEach workspace maintains its own set of windows.",
            "action": None,
        },
        {
            "title": "🤖  AI-Powered Desktop",
            "desc": "The desktop is infused with AI:\n• Smart Hub — context-aware suggestions\n• AI Search (Ctrl+K) — natural language\n• Smart Notifications — periodic tips\n• AI Context Menu — right-click analysis\n• Desktop Widgets — clock + weather",
            "action": None,
        },
        {
            "title": "✨  Thank You!",
            "desc": "NovaOS — Where AI meets the Desktop\n\n98 Python modules • 12 apps • 34 AI skills\n7 themes • Virtual desktops • Full terminal\nChromium browser • Music player • And more.\n\nBuilt as a college admission project.\n\n🚀  Run: python main.py",
            "action": None,
        },
    ]

    def __init__(self, master, kernel=None):
        super().__init__(master)
        self.kernel = kernel
        self.current_step = 0
        self._paused = False

        # Full screen overlay
        self.overrideredirect(True)
        self.configure(fg_color="#050810")
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"{screen_w}x{screen_h}+0+0")
        self.attributes("-topmost", True)

        self._build_ui()
        self._show_step(0)

    def _build_ui(self):
        # Progress dots at top
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.progress_frame.pack(fill="x", pady=(15, 0))
        self.progress_frame.pack_propagate(False)

        self.dots = []
        for i in range(len(self.FEATURES)):
            dot = ctk.CTkLabel(self.progress_frame, text="○",
                font=("Segoe UI", 12), text_color="#333333")
            dot.pack(side="left", padx=6)
            self.dots.append(dot)

        # Main content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=80)

        # Feature icon
        self.icon_label = ctk.CTkLabel(self.content_frame, text="",
            font=("Segoe UI Emoji", 72), text_color="#00E5FF")
        self.icon_label.pack(pady=(40, 10))

        # Feature title
        self.title_label = ctk.CTkLabel(self.content_frame, text="",
            font=("Segoe UI", 32, "bold"), text_color="#FFFFFF",
            wraplength=700)
        self.title_label.pack(pady=(0, 20))

        # Feature description
        self.desc_label = ctk.CTkLabel(self.content_frame, text="",
            font=("Segoe UI", 16), text_color="#AAAAAA",
            wraplength=600, justify="center")
        self.desc_label.pack()

        # Navigation buttons at bottom
        nav_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        nav_frame.pack(fill="x", side="bottom", padx=40, pady=20)
        nav_frame.pack_propagate(False)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(nav_frame, width=400, height=4,
            fg_color="#1A2332", progress_color="#00E5FF")
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)

        self.prev_btn = ctk.CTkButton(nav_frame, text="←  Previous", width=140, height=36,
            fg_color="#161B22", text_color="#888888", hover_color="#1C2333",
            corner_radius=8, font=("Segoe UI", 12),
            command=self._prev)
        self.prev_btn.pack(side="left")

        self.skip_btn = ctk.CTkButton(nav_frame, text="Skip Demo  ✕", width=140, height=36,
            fg_color="transparent", text_color="#555555", hover_color="#161B22",
            corner_radius=8, font=("Segoe UI", 12),
            command=self._close)
        self.skip_btn.pack(side="right")

        self.next_btn = ctk.CTkButton(nav_frame, text="Next  →", width=140, height=36,
            fg_color="#00E5FF", text_color="black", hover_color="#00C8E8",
            corner_radius=8, font=("Segoe UI", 12, "bold"),
            command=self._next)
        self.next_btn.pack(side="right", padx=(0, 15))

        # Keyboard shortcuts
        self.bind("<Right>", lambda e: self._next())
        self.bind("<Left>", lambda e: self._prev())
        self.bind("<Escape>", lambda e: self._close())
        self.bind("<Return>", lambda e: self._next())
        self.bind("<space>", lambda e: self._next())

        # Counter label
        self.counter_label = ctk.CTkLabel(nav_frame, text="1 / 15",
            font=("Segoe UI", 11), text_color="#555555")
        self.counter_label.pack(side="right", padx=(0, 15))

    def _show_step(self, index):
        if index < 0 or index >= len(self.FEATURES):
            return

        self.current_step = index
        step = self.FEATURES[index]

        # Update progress dots
        for i, dot in enumerate(self.dots):
            if i < index:
                dot.configure(text="●", text_color="#00E5FF")
            elif i == index:
                dot.configure(text="●", text_color="#FFFFFF")
            else:
                dot.configure(text="○", text_color="#333333")

        # Update content
        # Extract emoji icon from title
        title = step["title"]
        icon = title.split("  ")[0] if "  " in title else ""
        clean_title = "  ".join(title.split("  ")[1:]) if "  " in title else title

        self.icon_label.configure(text=icon)
        self.title_label.configure(text=clean_title)
        self.desc_label.configure(text=step["desc"])

        # Update progress bar
        self.progress_bar.set((index + 1) / len(self.FEATURES))

        # Update counter
        self.counter_label.configure(text=f"{index + 1} / {len(self.FEATURES)}")

        # Update button states
        self.prev_btn.configure(state="normal" if index > 0 else "disabled")

        if index == len(self.FEATURES) - 1:
            self.next_btn.configure(text="Finish  ✨", fg_color="#4CAF50")
        else:
            self.next_btn.configure(text="Next  →", fg_color="#00E5FF")

        # Execute action if any
        self._execute_action(step.get("action"))

    def _execute_action(self, action):
        """Execute a demo action (open an app, toggle a feature, etc.)."""
        if not self.kernel:
            return

        try:
            if action == "toggle_ai_panel":
                if hasattr(self.kernel, 'desktop'):
                    assistant = self.kernel.ai.assistant if hasattr(self.kernel, 'ai') and self.kernel.ai else None
                    self.kernel.desktop.toggle_ai_panel(assistant)

            elif action == "open_browser":
                self.kernel.process_manager.start_process("Browser")

            elif action == "open_notes":
                self.kernel.process_manager.start_process("Notes")

            elif action == "open_files":
                self.kernel.process_manager.start_process("Files")

            elif action == "open_terminal":
                self.kernel.process_manager.start_process("Terminal")

            elif action == "open_music":
                self.kernel.process_manager.start_process("Music Player")

            elif action == "open_weather":
                self.kernel.process_manager.start_process("Weather")

            elif action == "open_system_monitor":
                self.kernel.process_manager.start_process("System Monitor")

            elif action == "open_task_manager":
                self.kernel.process_manager.start_process("Task Manager")

            elif action == "open_calendar":
                self.kernel.process_manager.start_process("Calendar")

            elif action == "show_themes":
                self.kernel.process_manager.start_process("Settings")
        except Exception as e:
            print(f"[Demo] Action error: {e}")

    def _next(self):
        if self.current_step < len(self.FEATURES) - 1:
            self._show_step(self.current_step + 1)
        else:
            self._close()

    def _prev(self):
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _close(self):
        # Close all demo-opened apps
        if self.kernel and hasattr(self.kernel, 'window_manager'):
            wm = self.kernel.window_manager
            demo_apps = [
                "Browser", "Notes", "Calculator", "Files",
                "Terminal", "Music Player", "Weather",
                "System Monitor", "Task Manager", "Calendar",
                "Settings", "Viewer",
            ]
            for app_name in demo_apps:
                try:
                    for win in list(wm.windows):
                        title = win.title_label.cget("text") if hasattr(win, 'title_label') else ""
                        if app_name.lower() in title.lower():
                            wm.close_window(win)
                except Exception:
                    pass
        try:
            self.destroy()
        except Exception:
            pass
