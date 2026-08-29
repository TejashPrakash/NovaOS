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
        self.aliases = {
            "ll": "ls",
            "la": "ls",
            "cls": "clear",
            "q": "exit",
            "..": "cd ..",
            "~": "cd ~",
        }

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

        # Resolve aliases
        if cmd in self.aliases:
            resolved = self.aliases[cmd]
            command = resolved + (" " + " ".join(args) if args else "")
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
            "grep": self._cmd_grep,
            "alias": self._cmd_alias,
            "export": self._cmd_export,
            "env": self._cmd_env,
            "kill": self._cmd_kill,
            "ps": self._cmd_ps,
            "df": self._cmd_df,
            "du": self._cmd_du,
            "head": self._cmd_head,
            "tail": self._cmd_tail,
            "wc": self._cmd_wc,
            "sort": self._cmd_sort,
            "uniq": self._cmd_uniq,
            "find": self._cmd_find,
            "tree": self._cmd_tree,
            "curl": self._cmd_curl,
            "ping": self._cmd_ping,
            "ifconfig": self._cmd_ifconfig,
            "nano": self._cmd_nano,
            "vim": self._cmd_vim,
            "exit": self._cmd_exit,
            "about": self._cmd_about,
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
        self._write_line("")
        self._write_line("Aliases:", "#00E5FF")
        for alias, target in self.aliases.items():
            self._write_line(f"  {alias:<20} -> {target}", "#BBBBBB")

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
        valid = ["cyberpunk", "neon", "sunset", "ocean", "midnight", "forest", "arctic"]
        if theme not in valid:
            self._write_line(f"Unknown theme: {theme}. Options: {', '.join(valid)}", "#E53935")
            return
        if hasattr(self.window, 'kernel') and hasattr(self.window.kernel, 'desktop'):
            self.window.kernel.set_theme(theme)
            self._write_line(f"Theme changed to {theme}", "#00E676")
        else:
            self._write_line("Theme manager not available", "#FFC107")

    # =====================================================
    # Extended Commands
    # =====================================================

    def _cmd_grep(self, args):
        if len(args) < 2:
            self._write_line("Usage: grep <pattern> <file>", "#FFC107")
            return
        pattern, filepath = args[0], args[1]
        path = Path(filepath) if Path(filepath).is_absolute() else self.current_dir / filepath
        if not path.exists():
            self._write_line(f"grep: {filepath}: No such file", "#E53935")
            return
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if pattern.lower() in line.lower():
                    self._write_line(line, "#BBBBBB")
        except Exception as e:
            self._write_line(f"grep: {e}", "#E53935")

    def _cmd_alias(self, args):
        if not args:
            for alias, target in self.aliases.items():
                self._write_line(f"  {alias}='{target}'", "#BBBBBB")
            return
        if "=" in args[0]:
            name, target = args[0].split("=", 1)
            self.aliases[name] = target
            self._write_line(f"Alias set: {name}='{target}'", "#00E676")
        else:
            self._write_line(f"Usage: alias name='command'", "#FFC107")

    def _cmd_export(self, args):
        if not args:
            for k, v in os.environ.items():
                self._write_line(f"  {k}={v}", "#BBBBBB")
            return
        if "=" in args[0]:
            key, val = args[0].split("=", 1)
            os.environ[key] = val
            self._write_line(f"Exported: {key}={val}", "#00E676")
        else:
            self._write_line(f"Usage: export KEY=value", "#FFC107")

    def _cmd_env(self, args):
        for k, v in sorted(os.environ.items()):
            self._write_line(f"  {k}={v}", "#BBBBBB")

    def _cmd_kill(self, args):
        if not args:
            self._write_line("Usage: kill <PID>", "#FFC107")
            return
        try:
            import signal
            pid = int(args[0])
            os.kill(pid, signal.SIGTERM)
            self._write_line(f"Sent SIGTERM to PID {pid}", "#00E676")
        except ProcessLookupError:
            self._write_line(f"No such process: {args[0]}", "#E53935")
        except PermissionError:
            self._write_line(f"Permission denied: {args[0]}", "#E53935")
        except Exception as e:
            self._write_line(f"kill: {e}", "#E53935")

    def _cmd_ps(self, args):
        import psutil
        procs = []
        for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
            try:
                info = p.info
                procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        self._write_line(f"{'PID':>7}  {'CPU%':>6}  {'MEM%':>6}  NAME", "#00E5FF")
        for p in sorted(procs, key=lambda x: x.get("cpu_percent", 0) or 0, reverse=True)[:25]:
            pid = p.get("pid", 0)
            cpu = p.get("cpu_percent", 0) or 0
            mem = p.get("memory_percent", 0) or 0
            name = p.get("name", "?")
            self._write_line(f"{pid:>7}  {cpu:>5.1f}%  {mem:>5.1f}%  {name}", "#BBBBBB")

    def _cmd_df(self, args):
        import psutil
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                self._write_line(
                    f"  {part.device:<15} {usage.total // (1024**3):>5}G "
                    f"{usage.used // (1024**3):>5}G {usage.percent:>5.1f}%  {part.mountpoint}",
                    "#BBBBBB"
                )
            except PermissionError:
                pass

    def _cmd_du(self, args):
        target = self.current_dir if not args else (
            Path(args[0]) if Path(args[0]).is_absolute() else self.current_dir / args[0]
        )
        if not target.exists():
            self._write_line(f"du: {target}: No such file or directory", "#E53935")
            return
        if target.is_file():
            size = target.stat().st_size
            self._write_line(f"  {self._human_size(size):>10}  {target.name}", "#BBBBBB")
        else:
            total = 0
            for f in target.rglob("*"):
                if f.is_file():
                    total += f.stat().st_size
            self._write_line(f"  {self._human_size(total):>10}  {target.name}/", "#BBBBBB")

    def _cmd_head(self, args):
        if not args:
            self._write_line("Usage: head <file> [lines]", "#FFC107")
            return
        n = 10
        filepath = args[0]
        if len(args) >= 3 and args[1] == "-n":
            try: n = int(args[2])
            except: pass
        path = Path(filepath) if Path(filepath).is_absolute() else self.current_dir / filepath
        if not path.exists():
            self._write_line(f"head: {filepath}: No such file", "#E53935")
            return
        try:
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:n]:
                self._write_line(line, "#BBBBBB")
        except Exception as e:
            self._write_line(f"head: {e}", "#E53935")

    def _cmd_tail(self, args):
        if not args:
            self._write_line("Usage: tail <file> [lines]", "#FFC107")
            return
        n = 10
        filepath = args[0]
        if len(args) >= 3 and args[1] == "-n":
            try: n = int(args[2])
            except: pass
        path = Path(filepath) if Path(filepath).is_absolute() else self.current_dir / filepath
        if not path.exists():
            self._write_line(f"tail: {filepath}: No such file", "#E53935")
            return
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in lines[-n:]:
                self._write_line(line, "#BBBBBB")
        except Exception as e:
            self._write_line(f"tail: {e}", "#E53935")

    def _cmd_wc(self, args):
        if not args:
            self._write_line("Usage: wc <file>", "#FFC107")
            return
        path = Path(args[0]) if Path(args[0]).is_absolute() else self.current_dir / args[0]
        if not path.exists():
            self._write_line(f"wc: {args[0]}: No such file", "#E53935")
            return
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            lines = len(text.splitlines())
            words = len(text.split())
            chars = len(text)
            self._write_line(f"  {lines} {words} {chars} {args[0]}", "#BBBBBB")
        except Exception as e:
            self._write_line(f"wc: {e}", "#E53935")

    def _cmd_sort(self, args):
        if not args:
            self._write_line("Usage: sort <file>", "#FFC107")
            return
        path = Path(args[0]) if Path(args[0]).is_absolute() else self.current_dir / args[0]
        if not path.exists():
            self._write_line(f"sort: {args[0]}: No such file", "#E53935")
            return
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line in sorted(lines):
                self._write_line(line, "#BBBBBB")
        except Exception as e:
            self._write_line(f"sort: {e}", "#E53935")

    def _cmd_uniq(self, args):
        if not args:
            self._write_line("Usage: uniq <file>", "#FFC107")
            return
        path = Path(args[0]) if Path(args[0]).is_absolute() else self.current_dir / args[0]
        if not path.exists():
            self._write_line(f"uniq: {args[0]}: No such file", "#E53935")
            return
        try:
            prev = None
            for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if line != prev:
                    self._write_line(line, "#BBBBBB")
                    prev = line
        except Exception as e:
            self._write_line(f"uniq: {e}", "#E53935")

    def _cmd_find(self, args):
        if not args:
            self._write_line("Usage: find <name>", "#FFC107")
            return
        pattern = args[0]
        matches = []
        for f in self.current_dir.rglob("*"):
            if pattern.lower() in f.name.lower():
                matches.append(f)
        if not matches:
            self._write_line(f"No matches for '{pattern}'", "#FFC107")
        else:
            for m in matches[:30]:
                color = "#00E5FF" if m.is_dir() else "#BBBBBB"
                self._write_line(f"  {m.relative_to(self.current_dir)}", color)
            if len(matches) > 30:
                self._write_line(f"  ... and {len(matches) - 30} more", "#FFC107")

    def _cmd_tree(self, args):
        target = self.current_dir if not args else (
            Path(args[0]) if Path(args[0]).is_absolute() else self.current_dir / args[0]
        )
        if not target.exists():
            self._write_line(f"tree: {target}: No such directory", "#E53935")
            return
        self._write_line(target.name or str(target), "#00E5FF")
        self._tree_recursive(target, "", 3)

    def _tree_recursive(self, path, prefix, max_depth):
        if max_depth <= 0:
            return
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
        except PermissionError:
            return
        for i, item in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            color = "#00E5FF" if item.is_dir() else "#BBBBBB"
            self._write_line(f"  {prefix}{connector}{item.name}", color)
            if item.is_dir():
                extension = "    " if i == len(items) - 1 else "│   "
                self._tree_recursive(item, prefix + extension, max_depth - 1)

    def _cmd_curl(self, args):
        if not args:
            self._write_line("Usage: curl <url>", "#FFC107")
            return
        import requests
        try:
            url = args[0] if args[0].startswith(("http://", "https://")) else "https://" + args[0]
            resp = requests.get(url, timeout=10)
            self._write_line(f"HTTP {resp.status_code} | {len(resp.text)} bytes", "#00E5FF")
            for line in resp.text.splitlines()[:50]:
                self._write_line(line, "#BBBBBB")
            if len(resp.text.splitlines()) > 50:
                self._write_line("... (truncated)", "#FFC107")
        except Exception as e:
            self._write_line(f"curl: {e}", "#E53935")

    def _cmd_ping(self, args):
        if not args:
            self._write_line("Usage: ping <host>", "#FFC107")
            return
        host = args[0]
        try:
            result = subprocess.run(
                ["ping", "-n", "4", host],
                capture_output=True, text=True, timeout=15
            )
            for line in result.stdout.splitlines():
                self._write_line(line, "#BBBBBB")
        except FileNotFoundError:
            self._write_line(f"ping: command not found", "#E53935")
        except Exception as e:
            self._write_line(f"ping: {e}", "#E53935")

    def _cmd_ifconfig(self, args):
        import psutil
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for name, addr_list in addrs.items():
            is_up = stats.get(name)
            status = "UP" if is_up and is_up.isup else "DOWN"
            self._write_line(f"{name}: {status}", "#00E5FF")
            for addr in addr_list:
                if addr.family.name == "AF_INET":
                    self._write_line(f"  inet {addr.address}", "#BBBBBB")
                elif addr.family.name == "AF_INET6":
                    self._write_line(f"  inet6 {addr.address}", "#BBBBBB")

    def _cmd_nano(self, args):
        self._write_line("Tip: Use the Notes app for editing files.", "#FFC107")

    def _cmd_vim(self, args):
        self._write_line("Tip: Use the Notes app for editing files.", "#FFC107")

    def _cmd_exit(self, args):
        if hasattr(self.window, 'kernel') and hasattr(self.window.kernel, 'process_manager'):
            self.window.kernel.process_manager.stop_process("Terminal")
        else:
            self._write_line("Goodbye!", "#00E5FF")

    def _cmd_about(self, args):
        lines = [
            ("══════════════════════════════════════", "#7B61FF"),
            ("  NovaOS v0.1.0-alpha", "#00E5FF"),
            ("  AI-Powered Desktop Operating System", "#BBBBBB"),
            ("", ""),
            (f"  Python: {platform.python_version()}", "#888888"),
            (f"  System: {platform.system()} {platform.release()}", "#888888"),
            (f"  Machine: {platform.machine()}", "#888888"),
            (f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "#888888"),
            ("", ""),
            ("  Built with CustomTkinter + Python", "#BBBBBB"),
            ("  Powered by Gemini / Ollama AI", "#BBBBBB"),
            ("══════════════════════════════════════", "#7B61FF"),
        ]
        for text, color in lines:
            self._write_line(text, color)

    @staticmethod
    def _human_size(size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"

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