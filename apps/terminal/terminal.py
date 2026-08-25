import os
import subprocess
import sys
import platform
from datetime import datetime
from pathlib import Path

import customtkinter as ctk
from sdk.app import NovaApp
from core.theme import ThemeManager


class TerminalApp(NovaApp):
    """NovaOS Terminal with built-in commands and shell execution."""

    APP_NAME = "Terminal"
    APP_ICON = ">_"
    DEFAULT_WIDTH = 900
    DEFAULT_HEIGHT = 550

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self.current_dir = Path.home()
        self.command_history = []
        self.history_index = -1
        self.output_lines = []

    def build(self):
        # Output area
        self.output = ctk.CTkTextbox(
            self.content,
            fg_color="#0A0E14",
            text_color="#00E5FF",
            font=("Cascadia Code", 13),
            wrap="word",
            state="disabled",
            corner_radius=8
        )
        self.output.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Input area
        input_frame = ctk.CTkFrame(
            self.content, fg_color="#161B22", corner_radius=8
        )
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.prompt_label = ctk.CTkLabel(
            input_frame,
            text=self._get_prompt(),
            font=("Cascadia Code", 13, "bold"),
            text_color="#00E5FF",
            width=200,
            anchor="w"
        )
        self.prompt_label.pack(side="left", padx=(10, 0))

        self.input_entry = ctk.CTkEntry(
            input_frame,
            fg_color="transparent",
            text_color="#FFFFFF",
            font=("Cascadia Code", 13),
            border_width=0,
            placeholder_text="Type a command..."
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5, pady=8)
        self.input_entry.bind("<Return>", self._execute_command)
        self.input_entry.bind("<Up>", self._history_up)
        self.input_entry.bind("<Down>", self._history_down)
        self.input_entry.bind("<Tab>", self._tab_complete)

        # Welcome message
        self._print_welcome()
        self.input_entry.focus()

    def _get_prompt(self):
        short_dir = str(self.current_dir).replace(
            str(Path.home()), "~"
        )
        return f"nova@os {short_dir} $ "

    def _print_welcome(self):
        self._write_line(
            "╔══════════════════════════════════════════╗",
            "#7B61FF"
        )
        self._write_line(
            "║         NovaOS Terminal v1.0.0           ║",
            "#00E5FF"
        )
        self._write_line(
            "║   Type 'help' for available commands     ║",
            "#888888"
        )
        self._write_line(
            "╚══════════════════════════════════════════╝",
            "#7B61FF"
        )
        self._write_line("")

    def _write_line(self, text, color="#BBBBBB"):
        self.output.configure(state="normal")
        self.output.insert("end", text + "\n", ("line",))
        self.output.tag_config("line", foreground=color)
        self.output.configure(state="disabled")
        self.output.see("end")

    def _execute_command(self, event=None):
        command = self.input_entry.get().strip()
        self.input_entry.delete(0, "end")

        if not command:
            return

        self.command_history.append(command)
        self.history_index = len(self.command_history)

        # Show command in output
        self._write_line(f"{self._get_prompt()}{command}", "#FFFFFF")

        # Route to built-in or system command
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        builtins = {
            "help": self._cmd_help,
            "clear": self._cmd_clear,
            "cd": self._cmd_cd,
            "pwd": self._cmd_pwd,
            "echo": self._cmd_echo,
            "date": self._cmd_date,
            "whoami": self._cmd_whoami,
            "uname": self._cmd_uname,
            "ls": self._cmd_ls,
            "cat": self._cmd_cat,
            "mkdir": self._cmd_mkdir,
            "touch": self._cmd_touch,
            "rm": self._cmd_rm,
            "history": self._cmd_history,
            "neofetch": self._cmd_neofetch,
            "theme": self._cmd_theme,
        }

        if cmd in builtins:
            try:
                builtins[cmd](args)
            except Exception as e:
                self._write_line(f"Error: {e}", "#E53935")
        else:
            self._run_system_command(command)

        self.prompt_label.configure(text=self._get_prompt())

    def _run_system_command(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(self.current_dir),
                timeout=15
            )
            if result.stdout:
                for line in result.stdout.rstrip().split("\n"):
                    self._write_line(line, "#BBBBBB")
            if result.stderr:
                for line in result.stderr.rstrip().split("\n"):
                    self._write_line(line, "#E53935")
            if result.returncode != 0 and not result.stderr:
                self._write_line(
                    f"Command exited with code {result.returncode}",
                    "#FFC107"
                )
        except subprocess.TimeoutExpired:
            self._write_line("Command timed out (15s limit)", "#E53935")
        except FileNotFoundError:
            self._write_line(
                f"Command not found: {command.split()[0]}", "#E53935"
            )
        except Exception as e:
            self._write_line(f"Error: {e}", "#E53935")

    # =====================================================
    # Built-in Commands
    # =====================================================

    def _cmd_help(self, args):
        commands = [
            ("help", "Show this help message"),
            ("clear", "Clear the terminal"),
            ("cd <dir>", "Change directory"),
            ("pwd", "Print working directory"),
            ("ls", "List files"),
            ("cat <file>", "Display file contents"),
            ("mkdir <dir>", "Create directory"),
            ("touch <file>", "Create empty file"),
            ("rm <path>", "Remove file or directory"),
            ("echo <text>", "Print text"),
            ("date", "Show current date/time"),
            ("whoami", "Show current user"),
            ("uname", "Show system info"),
            ("history", "Show command history"),
            ("neofetch", "System information"),
            ("theme <name>", "Change theme"),
        ]
        self._write_line("Available commands:", "#00E5FF")
        self._write_line("")
        for cmd, desc in commands:
            self._write_line(f"  {cmd:<20} {desc}", "#BBBBBB")

    def _cmd_clear(self, args):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def _cmd_cd(self, args):
        if not args:
            self.current_dir = Path.home()
            return
        target = Path(args[0]).expanduser()
        if not target.is_absolute():
            target = self.current_dir / target
        if target.exists() and target.is_dir():
            self.current_dir = target.resolve()
        else:
            self._write_line(f"cd: no such directory: {args[0]}", "#E53935")

    def _cmd_pwd(self, args):
        self._write_line(str(self.current_dir), "#BBBBBB")

    def _cmd_echo(self, args):
        self._write_line(" ".join(args), "#BBBBBB")

    def _cmd_date(self, args):
        now = datetime.now()
        self._write_line(now.strftime("%a %b %d %H:%M:%S %Y"), "#BBBBBB")

    def _cmd_whoami(self, args):
        self._write_line(platform.node(), "#BBBBBB")

    def _cmd_uname(self, args):
        info = f"{platform.system()} {platform.release()} {platform.machine()}"
        self._write_line(info, "#BBBBBB")

    def _cmd_ls(self, args):
        try:
            items = sorted(self.current_dir.iterdir(),
                           key=lambda x: (x.is_file(), x.name.lower()))
            for item in items:
                prefix = "📁 " if item.is_dir() else "📄 "
                color = "#00E5FF" if item.is_dir() else "#BBBBBB"
                self._write_line(f"{prefix}{item.name}", color)
        except PermissionError:
            self._write_line("Permission denied", "#E53935")

    def _cmd_cat(self, args):
        if not args:
            self._write_line("cat: missing file operand", "#E53935")
            return
        path = Path(args[0])
        if not path.is_absolute():
            path = self.current_dir / path
        if not path.exists():
            self._write_line(f"cat: {args[0]}: No such file", "#E53935")
            return
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            for line in text.splitlines():
                self._write_line(line, "#BBBBBB")
        except Exception as e:
            self._write_line(f"cat: {e}", "#E53935")

    def _cmd_mkdir(self, args):
        if not args:
            self._write_line("mkdir: missing operand", "#E53935")
            return
        try:
            (self.current_dir / args[0]).mkdir(exist_ok=True)
        except Exception as e:
            self._write_line(f"mkdir: {e}", "#E53935")

    def _cmd_touch(self, args):
        if not args:
            self._write_line("touch: missing operand", "#E53935")
            return
        try:
            (self.current_dir / args[0]).touch()
        except Exception as e:
            self._write_line(f"touch: {e}", "#E53935")

    def _cmd_rm(self, args):
        if not args:
            self._write_line("rm: missing operand", "#E53935")
            return
        target = self.current_dir / args[0]
        if not target.exists():
            self._write_line(f"rm: {args[0]}: No such file", "#E53935")
            return
        try:
            if target.is_dir():
                import shutil
                shutil.rmtree(target)
            else:
                target.unlink()
        except Exception as e:
            self._write_line(f"rm: {e}", "#E53935")

    def _cmd_history(self, args):
        for i, cmd in enumerate(self.command_history, 1):
            self._write_line(f"  {i:>4}  {cmd}", "#BBBBBB")

    def _cmd_neofetch(self, args):
        lines = [
            ("       ◈◈◈        ", "#00E5FF", "nova@os", "#00E5FF"),
            ("     ◈◈◈◈◈◈◈      ", "#00E5FF", f"OS: NovaOS v0.1.0", "#BBBBBB"),
            ("    ◈◈◈◈◈◈◈◈◈     ", "#00E5FF", f"Host: {platform.node()}", "#BBBBBB"),
            ("     ◈◈◈◈◈◈◈      ", "#7B61FF", f"Kernel: {platform.system()} {platform.release()}", "#BBBBBB"),
            ("       ◈◈◈        ", "#FF00E5", f"Shell: NovaOS Terminal", "#BBBBBB"),
            ("                   ", "", f"Theme: Cyberpunk", "#BBBBBB"),
            ("                   ", "", f"Python: {platform.python_version()}", "#BBBBBB"),
            ("                  ", "", f"Machine: {platform.machine()}", "#BBBBBB"),
        ]
        for deco, dcolor, info, icolor in lines:
            self._write_line(f"  {deco}  {info}", icolor if deco.strip() else icolor)

    def _cmd_theme(self, args):
        if not args:
            self._write_line("Usage: theme <cyberpunk|neon|sunset|ocean>", "#FFC107")
            return
        theme = args[0].lower()
        valid = ["cyberpunk", "neon", "sunset", "ocean"]
        if theme not in valid:
            self._write_line(f"Unknown theme: {theme}. Options: {', '.join(valid)}", "#E53935")
            return
        if hasattr(self.window, 'kernel') and hasattr(self.window.kernel, 'desktop'):
            self.window.kernel.set_theme(theme)
            self._write_line(f"Theme changed to {theme}", "#00E676")
        else:
            self._write_line("Theme manager not available", "#FFC107")

    # =====================================================
    # History Navigation
    # =====================================================

    def _history_up(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, self.command_history[self.history_index])

    def _history_down(self, event):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.input_entry.delete(0, "end")

    def _tab_complete(self, event):
        partial = self.input_entry.get()
        if not partial:
            return
        parts = partial.split()
        if len(parts) < 2:
            # Complete command names
            commands = ["help", "clear", "cd", "pwd", "ls", "cat",
                        "mkdir", "touch", "rm", "echo", "date",
                        "whoami", "uname", "history", "neofetch", "theme"]
            matches = [c for c in commands if c.startswith(parts[0])]
            if len(matches) == 1:
                self.input_entry.delete(0, "end")
                self.input_entry.insert(0, matches[0] + " ")
        else:
            # Complete file/directory names
            partial_name = parts[-1]
            try:
                candidates = [
                    item.name for item in self.current_dir.iterdir()
                    if item.name.startswith(partial_name)
                ]
                if len(candidates) == 1:
                    completed = candidates[0]
                    prefix = " " if len(parts) > 1 else ""
                    self.input_entry.delete(0, "end")
                    self.input_entry.insert(
                        0,
                        " ".join(parts[:-1]) + " " + completed
                    )
            except Exception:
                pass