"""Virtual Desktops — compact inline workspace switcher for the dock."""

import customtkinter as ctk


class VirtualDesktopSwitcher(ctk.CTkFrame):
    """Tiny inline workspace indicator embedded in the dock."""

    DESKTOP_COUNT = 4

    def __init__(self, master, kernel=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.kernel = kernel
        self.workspaces = [[] for _ in range(self.DESKTOP_COUNT)]
        self.active = 0

        self.configure(height=50)
        self.pack_propagate(False)

        self._build_ui()

    def _build_ui(self):
        # Thin separator line on the left
        sep = ctk.CTkFrame(self, fg_color="#333333", width=1, height=30)
        sep.pack(side="left", padx=(0, 8), pady=10)

        # Label
        ctk.CTkLabel(
            self, text="WS",
            font=("Segoe UI", 9, "bold"),
            text_color="#555555",
            width=22
        ).pack(side="left", padx=(0, 4), pady=10)

        # Dot buttons
        self.ws_buttons = []
        for i in range(self.DESKTOP_COUNT):
            btn = ctk.CTkButton(
                self,
                text=str(i + 1),
                width=28,
                height=28,
                corner_radius=14,
                fg_color="#00E5FF" if i == self.active else "#1A2332",
                text_color="#000000" if i == self.active else "#555555",
                hover_color="#00B8D4" if i == self.active else "#252B3B",
                font=("Segoe UI", 10, "bold"),
                command=lambda idx=i: self.switch_to(idx),
                border_width=1,
                border_color="#00E5FF" if i == self.active else "#2A2A2A"
            )
            btn.pack(side="left", padx=2, pady=10)
            self.ws_buttons.append(btn)

        # Thin separator on the right
        sep2 = ctk.CTkFrame(self, fg_color="#333333", width=1, height=30)
        sep2.pack(side="left", padx=(8, 0), pady=10)

    def switch_to(self, index):
        """Switch to a different workspace."""
        if index == self.active or index < 0 or index >= self.DESKTOP_COUNT:
            return

        old_active = self.active
        self.active = index

        # Update button styles
        for i, btn in enumerate(self.ws_buttons):
            if i == index:
                btn.configure(
                    fg_color="#00E5FF",
                    text_color="#000000",
                    border_color="#00E5FF",
                    hover_color="#00B8D4"
                )
            else:
                btn.configure(
                    fg_color="#1A2332",
                    text_color="#555555",
                    border_color="#2A2A2A",
                    hover_color="#252B3B"
                )

        self._apply_workspace(index, old_active)

    def _apply_workspace(self, new_ws, old_ws):
        """Show windows belonging to new_ws, hide old_ws windows."""
        if not self.kernel or not self.kernel.window_manager:
            return
        wm = self.kernel.window_manager

        # WindowManager.windows is a list of AppWindow objects;
        # we stored id(window) as the identifier.
        windows_by_id = {id(w): w for w in wm.windows}

        # Hide old workspace windows
        for wid in self.workspaces[old_ws]:
            win = windows_by_id.get(wid)
            if win:
                try:
                    win.withdraw()
                except Exception:
                    pass

        # Show new workspace windows
        for wid in self.workspaces[new_ws]:
            win = windows_by_id.get(wid)
            if win:
                try:
                    win.deiconify()
                    win.lift()
                except Exception:
                    pass

    def register_window(self, window_id):
        """Register a window ID to the active workspace."""
        for ws in self.workspaces:
            if window_id in ws:
                ws.remove(window_id)
        self.workspaces[self.active].append(window_id)

    def unregister_window(self, window_id):
        """Remove a window from all workspaces."""
        for ws in self.workspaces:
            if window_id in ws:
                ws.remove(window_id)

    def get_active(self):
        return self.active
