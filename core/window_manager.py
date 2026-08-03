import math
import customtkinter as ctk

from apps.registry import APP_REGISTRY


class AppWindow(ctk.CTkFrame):
    """
    Floating application window inside the NovaOS desktop.
    """

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
        self.app = None

        # Remember each app's original preferred size.
        self.requested_width = width
        self.requested_height = height

        self.place(
            x=manager.WINDOW_MARGIN,
            y=manager.WINDOW_MARGIN
        )

        # App widgets must not resize the outer NovaOS window.
        self.pack_propagate(False)

        # ======================================
        # Title Bar
        # ======================================

        self.titlebar = ctk.CTkFrame(
            self,
            height=42,
            fg_color="#252B3B",
            corner_radius=16
        )
        self.titlebar.pack(fill="x")
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

        # ======================================
        # App Content
        # ======================================

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.pack(
            fill="both",
            expand=True
        )

        # ======================================
        # Window Dragging
        # ======================================

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
            lambda event: self.focus_window()
        )

        self.content.bind(
            "<Button-1>",
            lambda event: self.focus_window()
        )

        self.lift()

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

        desktop_width, work_height = self.manager.get_work_area()
        margin = self.manager.WINDOW_MARGIN

        max_x = max(
            margin,
            desktop_width - self.winfo_width() - margin
        )

        max_y = max(
            margin,
            work_height - self.winfo_height() - margin
        )

        x = max(margin, min(x, max_x))
        y = max(margin, min(y, max_y))

        self.place(x=x, y=y)


# =========================================================


class WindowManager:
    """
    Creates, positions, tiles, focuses, and closes NovaOS windows.
    """

    WINDOW_MARGIN = 16
    DOCK_SAFE_GAP = 20

    def __init__(self, desktop, dock, kernel):
        self.desktop = desktop
        self.dock = dock
        self.kernel = kernel
        self.windows = []

    # =====================================================

    def get_work_area(self):
        """
        Return the usable desktop area, excluding the dock.
        """

        canvas = self.desktop.get_canvas()
        canvas.update_idletasks()

        desktop_width = canvas.winfo_width()
        desktop_height = canvas.winfo_height()

        # Fallback while Tkinter is still rendering the UI.
        if desktop_width <= 1:
            desktop_width = canvas.winfo_toplevel().winfo_width()

        if desktop_height <= 1:
            desktop_height = canvas.winfo_toplevel().winfo_height()

        dock_height = self.dock.frame.winfo_height()

        if dock_height <= 1:
            dock_height = int(self.dock.frame.cget("height"))

        work_height = (
            desktop_height
            - dock_height
            - self.DOCK_SAFE_GAP
        )

        return desktop_width, work_height

    # =====================================================

    def fit_window_size(self, width, height):
        """
        Prevent a single window from exceeding the usable desktop.
        """

        desktop_width, work_height = self.get_work_area()
        margin = self.WINDOW_MARGIN

        max_width = max(
            320,
            desktop_width - (margin * 2)
        )

        max_height = max(
            240,
            work_height - (margin * 2)
        )

        return min(width, max_width), min(height, max_height)

    # =====================================================

    def arrange_windows(self):
        """
        Keep one window at its preferred size.
        Tile two or more windows without overlap.
        """

        if not self.windows:
            return

        desktop_width, work_height = self.get_work_area()
        margin = self.WINDOW_MARGIN
        count = len(self.windows)

        # A single window uses the app's preferred dimensions.
        if count == 1:
            window = self.windows[0]

            width, height = self.fit_window_size(
                window.requested_width,
                window.requested_height
            )

            x = max(
                margin,
                (desktop_width - width) // 2
            )

            y = margin

            window.configure(
                width=width,
                height=height
            )

            window.place(
                x=x,
                y=y
            )

            return

        # Two or more apps use a responsive two-column grid.
        columns = 2
        rows = math.ceil(count / columns)

        cell_width = (
            desktop_width - (margin * (columns + 1))
        ) // columns

        cell_height = (
            work_height - (margin * (rows + 1))
        ) // rows

        for index, window in enumerate(self.windows):
            row = index // columns
            column = index % columns

            x = margin + column * (cell_width + margin)
            y = margin + row * (cell_height + margin)

            window.configure(
                width=cell_width,
                height=cell_height
            )

            window.place(
                x=x,
                y=y
            )

    # =====================================================

    def create_window(
        self,
        title,
        width=None,
        height=None,
        launch_app=True
    ):
        if title in APP_REGISTRY:
            app_class = APP_REGISTRY[title]

            if width is None:
                width = app_class.DEFAULT_WIDTH

            if height is None:
                height = app_class.DEFAULT_HEIGHT

        if width is None:
            width = 520

        if height is None:
            height = 360

        width, height = self.fit_window_size(width, height)

        # Do not open a duplicate window for the same app.
        for window in self.windows:
            if window.title == title:
                window.focus_window()
                return window

        window = AppWindow(
            self,
            title,
            width,
            height
        )

        self.windows.append(window)

        if launch_app and title in APP_REGISTRY:
            app = APP_REGISTRY[title](window)
            window.app = app
            app.build()

        self.arrange_windows()

        self.kernel.events.emit(
            "window_created",
            window
        )

        self.dock.add_app(
            title,
            window.focus_window
        )

        return window

    # =====================================================

    def close_window(self, window):
        if window not in self.windows:
            return

        self.windows.remove(window)

        self.dock.remove_app(
            window.title
        )

        window.destroy()

        # Reflow remaining windows after one closes.
        self.arrange_windows()