import customtkinter as ctk

# ==========================================================
# Constants
# ==========================================================

WINDOW_START_X = 180
WINDOW_START_Y = 100

CASCADE_OFFSET = 35

MAX_CASCADE_X = 450
MAX_CASCADE_Y = 250


# ==========================================================
# App Window
# ==========================================================

class AppWindow(ctk.CTkFrame):

    def __init__(
        self,
        manager,
        title="Application",
        width=500,
        height=350
    ):

        super().__init__(
            manager.desktop,
            width=width,
            height=height,
            fg_color="#1A1F2B",
            corner_radius=12,
            border_width=1,
            border_color="#2F3545"
        )

        self.manager = manager

        self.title = title

        self.is_minimized = False
        self.is_maximized = False

        self.drag_x = 0
        self.drag_y = 0

        # ----------------------------------------------------
        # Window Position
        # ----------------------------------------------------

        self.place(
            x=manager.next_x,
            y=manager.next_y
        )

        manager.next_x += CASCADE_OFFSET
        manager.next_y += CASCADE_OFFSET

        if manager.next_x > MAX_CASCADE_X:
            manager.next_x = WINDOW_START_X

        if manager.next_y > MAX_CASCADE_Y:
            manager.next_y = WINDOW_START_Y

        # =====================================================
        # Title Bar
        # =====================================================

        self.titlebar = ctk.CTkFrame(
            self,
            height=40,
            fg_color="#252B3B",
            corner_radius=12
        )

        self.titlebar.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.titlebar,
            text=title,
            font=("Segoe UI", 15, "bold")
        )

        self.title_label.pack(
            side="left",
            padx=15
        )

        # =====================================================
        # Close Button
        # =====================================================

        self.close_btn = ctk.CTkButton(
            self.titlebar,
            text="✕",
            width=35,
            fg_color="#E53935",
            hover_color="#C62828",
            command=self.close
        )

        self.close_btn.pack(
            side="right",
            padx=8,
            pady=4
        )

        # =====================================================
        # Content Area
        # =====================================================

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # Bindings
        # =====================================================

        self.titlebar.bind("<Button-1>", self.start_move)
        self.titlebar.bind("<B1-Motion>", self.do_move)

        self.bind("<Button-1>", self.focus)
        self.content.bind("<Button-1>", self.focus)
        self.title_label.bind("<Button-1>", self.focus)

    # =====================================================
    # Focus
    # =====================================================

    def focus(self, event=None):

        self.manager.focus_window(self)

    # =====================================================
    # Close
    # =====================================================

    def close(self):

        self.manager.close_window(self)

    # =====================================================
    # Drag
    # =====================================================

    def start_move(self, event):

        self.focus()

        self.drag_x = event.x
        self.drag_y = event.y

    def do_move(self, event):

        x = self.winfo_x() + event.x - self.drag_x
        y = self.winfo_y() + event.y - self.drag_y

        self.place(
            x=x,
            y=y
        )


# ==========================================================
# Window Manager
# ==========================================================

class WindowManager:

    def __init__(self, desktop, taskbar):

        self.desktop = desktop
        self.taskbar = taskbar

        self.windows = []

        self.active_window = None

        self.next_x = WINDOW_START_X
        self.next_y = WINDOW_START_Y

    # =====================================================
    # Create Window
    # =====================================================

    def create_window(
        self,
        title="Application",
        width=500,
        height=350
    ):

        window = AppWindow(
            self,
            title,
            width,
            height
        )

        self.windows.append(window)
        self.taskbar.add_app(window)

        self.focus_window(window)

        return window

    # =====================================================
    # Focus Window
    # =====================================================

    def focus_window(self, window):

        if window not in self.windows:
            return

        self.active_window = window

        window.lift()

    # =====================================================
    # Close Window
    # =====================================================

    def close_window(self, window):

        if window in self.windows:

            self.windows.remove(window)

        self.taskbar.remove_app(window)
        window.destroy()

        if self.windows:

            self.focus_window(
                self.windows[-1]
            )

        else:

            self.active_window = None