import customtkinter as ctk


class AppWindow(ctk.CTkFrame):

    def __init__(
        self,
        manager,
        title,
        width=520,
        height=360
    ):

        super().__init__(
            manager.desktop.get_canvas(),
            width=width,
            height=height,
            fg_color="#1A1F2B",
            corner_radius=16,
            border_width=1,
            border_color="#2F3545"
        )

        self.manager = manager
        self.title = title

        self.place(
            x=manager.next_x,
            y=manager.next_y
        )

        self.lift()

        manager.next_x += 35
        manager.next_y += 35

        if manager.next_x > 500:
            manager.next_x = 150

        if manager.next_y > 250:
            manager.next_y = 80

        # ======================================
        # Title Bar
        # ======================================

        self.titlebar = ctk.CTkFrame(
            self,
            height=42,
            fg_color="#252B3B",
            corner_radius=16
        )

        self.titlebar.pack(
            fill="x"
        )

        self.titlebar.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.titlebar,
            text=title,
            font=("Segoe UI", 15, "bold")
        )

        self.title_label.pack(
            side="left",
            padx=15
        )

        # -----------------------------
        # Close
        # -----------------------------

        self.close_btn = ctk.CTkButton(
            self.titlebar,
            text="✕",
            width=32,
            fg_color="#E53935",
            hover_color="#C62828",
            command=self.close
        )

        self.close_btn.pack(
            side="right",
            padx=6,
            pady=5
        )

        # -----------------------------
        # Content
        # -----------------------------

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        # -----------------------------
        # Dragging
        # -----------------------------

        self.titlebar.bind(
            "<Button-1>",
            self.start_move
        )

        self.titlebar.bind(
            "<B1-Motion>",
            self.do_move
        )

        self.bind(
            "<Button-1>",
            lambda e: self.focus_window()
        )

        self.content.bind(
            "<Button-1>",
            lambda e: self.focus_window()
        )

    # =====================================================

    def focus_window(self):

        self.lift()

        self.focus_force()
        
    # =====================================================

    def close(self):

        self.manager.close_window(self)

    # =====================================================

    def start_move(self, event):

        self.focus_window()

        self._x = event.x

        self._y = event.y

    # =====================================================

    def do_move(self, event):

        x = self.winfo_x() + event.x - self._x

        y = self.winfo_y() + event.y - self._y

        self.place(
            x=x,
            y=y
        )


# =========================================================


class WindowManager:

    def __init__(
        self,
        desktop,
        dock
    ):

        self.desktop = desktop

        self.dock = dock

        self.windows = []

        self.next_x = 150

        self.next_y = 80

    # =====================================================

    def create_window(
        self,
        title,
        width=520,
        height=360
    ):

        # ----------------------------------
        # Already running?
        # ----------------------------------

        for window in self.windows:

            if window.title == title:

                window.focus_window()

                return window

        # ----------------------------------
        # Create new window
        # ----------------------------------

        window = AppWindow(
            self,
            title,
            width,
            height
        )

        self.windows.append(window)

        self.dock.add_app(
            title,
            window.focus_window
        )

        return window

    # =====================================================

    def close_window(
        self,
        window
    ):

        if window in self.windows:

            self.windows.remove(window)

            self.dock.remove_app(
                window.title
            )

            window.destroy()