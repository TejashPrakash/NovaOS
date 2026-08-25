import math
import json
import os
import customtkinter as ctk

from apps.registry import APP_REGISTRY
from core.theme import ThemeManager
from widgets.glass import GlassFrame


class AppWindow(GlassFrame):
    """Premium glassmorphism application window inside NovaOS desktop."""
    def __init__(
        self,
        manager,
        title,
        width=520,
        height=360
    ):
        self.theme = ThemeManager()
        super().__init__(
            manager.desktop.get_canvas(),
            width=width,
            height=height,
            blur_amount=15,
            opacity=0.95,
            fg_color=self.theme.get_color("surface"),
            corner_radius=16,
            border_width=2,
            border_color=self.theme.get_color("primary")
        )
        self.manager = manager
        self.title = title
        self.app = None
        self.requested_width = width
        self.requested_height = height
        self._target_x = None
        self._target_y = None
        self._target_width = None
        self._target_height = None
        self._animation_steps = 0
        self._total_animation_steps = 10
        self.tabs = []
        self.current_tab = None
        self.tab_frame = None
        
        self.place(
            x=manager.WINDOW_MARGIN,
            y=manager.WINDOW_MARGIN
        )
        self.pack_propagate(False)
        self._setup_titlebar()
        self._setup_content()
        self._setup_dragging()
        self.lift()
        
    def _setup_titlebar(self):
        """Setup title bar with window controls and tabs."""
        self.titlebar = ctk.CTkFrame(
            self,
            height=42,
            fg_color=self.theme.get_color("surface_light"),
            corner_radius=16
        )
        self.titlebar.pack(fill="x")
        self.titlebar.pack_propagate(False)
        
        # Setup tabs
        self._setup_tabs()
        
        self.title_label = ctk.CTkLabel(
            self.titlebar,
            text=self.title,
            font=("Segoe UI", 15, "bold"),
            text_color=self.theme.get_color("primary")
        )
        self.title_label.pack(side="left", padx=15)
        
        # Window controls
        controls_frame = ctk.CTkFrame(
            self.titlebar,
            fg_color="transparent"
        )
        controls_frame.pack(side="right", padx=6, pady=5)
        
        # Minimize button
        self.minimize_btn = ctk.CTkButton(
            controls_frame,
            text="─",
            width=32,
            fg_color="#FFA500",
            hover_color="#FB8C00",
            corner_radius=6,
            command=self.minimize
        )
        self.minimize_btn.pack(side="right", padx=2)
        
        # Maximize button
        self.maximize_btn = ctk.CTkButton(
            controls_frame,
            text="□",
            width=32,
            fg_color=self.theme.get_color("primary"),
            hover_color=self.theme.get_color("primary_hover"),
            corner_radius=6,
            command=self.toggle_maximize
        )
        self.maximize_btn.pack(side="right", padx=2)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            controls_frame,
            text="✕",
            width=32,
            fg_color=self.theme.get_color("error"),
            hover_color="#C62828",
            corner_radius=6,
            command=self.close
        )
        self.close_btn.pack(side="right", padx=2)
        
        self.is_maximized = False
        self.is_minimized = False
        self.restore_geometry = None
        
    def _setup_content(self):
        """Setup app content area."""
        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content.pack(fill="both", expand=True)
        self._setup_resize_handles()

    def _setup_tabs(self):
        """Setup tab management for the window."""
        self.tab_frame = ctk.CTkFrame(
            self.titlebar,
            fg_color="transparent"
        )
        self.tab_frame.pack(side="left", padx=10, fill="y")
        
        self.add_tab("Main")

    def add_tab(self, tab_name):
        """Add a new tab to the window."""
        tab_button = ctk.CTkButton(
            self.tab_frame,
            text=tab_name,
            width=80,
            height=30,
            fg_color=self.theme.get_color("surface_light"),
            text_color=self.theme.get_color("text_primary"),
            hover_color=self.theme.get_color("primary"),
            corner_radius=6,
            command=lambda: self.switch_tab(tab_name)
        )
        tab_button.pack(side="left", padx=2)
        self.tabs.append({"name": tab_name, "button": tab_button})
        
        if len(self.tabs) == 1:
            self.switch_tab(tab_name)

    def switch_tab(self, tab_name):
        """Switch to a specific tab."""
        self.current_tab = tab_name
        for tab in self.tabs:
            if tab["name"] == tab_name:
                tab["button"].configure(
                    fg_color=self.theme.get_color("primary"),
                    text_color="white"
                )
            else:
                tab["button"].configure(
                    fg_color=self.theme.get_color("surface_light"),
                    text_color=self.theme.get_color("text_primary")
                )

    def _setup_dragging(self):
        """Setup window dragging."""
        self.titlebar.bind("<Button-1>", self.start_move)
        self.titlebar.bind("<B1-Motion>", self.do_move)
        self.bind("<Button-1>", lambda event: self.focus_window())
        self.content.bind("<Button-1>", lambda event: self.focus_window())

    def _setup_resize_handles(self):
        """Setup window resize handles."""
        self.resize_handle = ctk.CTkFrame(
            self,
            width=20,
            height=20,
            fg_color=self.theme.get_color("primary"),
            corner_radius=0
        )
        self.resize_handle.place(relx=1, rely=1, anchor="se")
        self.resize_handle.bind("<B1-Motion>", self._do_resize)
        self.resize_handle.bind("<Button-1>", self._start_resize)

    def _start_resize(self, event):
        """Start window resizing."""
        self._resize_start_x = event.x
        self._resize_start_y = event.y
        self._resize_start_width = self.winfo_width()
        self._resize_start_height = self.winfo_height()

    def _do_resize(self, event):
        """Handle window resizing."""
        delta_x = event.x - self._resize_start_x
        delta_y = event.y - self._resize_start_y

        new_width = max(320, self._resize_start_width + delta_x)
        new_height = max(240, self._resize_start_height + delta_y)

        self.configure(width=new_width, height=new_height)

    def animate_to(self, x, y, width=None, height=None):
        """Animate window to new position/size."""
        self._target_x = x
        self._target_y = y
        self._target_width = width or self.winfo_width()
        self._target_height = height or self.winfo_height()
        self._animation_steps = 0
        self._animate()
        
    def _animate(self):
        """Perform animation step."""
        if self._animation_steps >= self._total_animation_steps:
            return
            
        progress = self._animation_steps / self._total_animation_steps
        eased_progress = self._ease_out_cubic(progress)
        
        current_x = self.winfo_x()
        current_y = self.winfo_y()
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        
        new_x = current_x + (self._target_x - current_x) * eased_progress
        new_y = current_y + (self._target_y - current_y) * eased_progress
        new_width = current_width + (self._target_width - current_width) * eased_progress
        new_height = current_height + (self._target_height - current_height) * eased_progress
        
        self.place(x=int(new_x), y=int(new_y))
        self.configure(width=int(new_width), height=int(new_height))
        
        self._animation_steps += 1
        self.after(16, self._animate)  # ~60 FPS
        
    def _ease_out_cubic(self, t: float) -> float:
        """Cubic easing out function."""
        return 1 - pow(1 - t, 3)
        
    def focus_window(self):
        """Focus window and bring to front."""
        self.lift()
        self.focus_force()
        
    def close(self):
        """Close window and save state."""
        self.manager.save_window_state(self.title, self)
        self.manager.close_window(self)
        
    def _destroy(self):
        """Actually destroy the window."""
        self.manager.close_window(self)

    def minimize(self):
        """Minimize window."""
        self.is_minimized = True
        self.restore_geometry = (self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height())
        self.place_forget()

    def restore(self):
        """Restore window to previous size."""
        if self.restore_geometry:
            x, y, width, height = self.restore_geometry
            self.animate_to(x, y, width, height)
            self.is_maximized = False
            self.is_minimized = False

    def toggle_maximize(self):
        """Toggle maximize state."""
        if self.is_minimized:
            self.restore()
        elif self.is_maximized:
            self.restore()
        else:
            self.maximize()

    def maximize(self):
        """Maximize window to desktop size."""
        self.is_maximized = True
        self.restore_geometry = (self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height())
        
        desktop_width, work_height = self.manager.get_work_area()
        margin = self.manager.WINDOW_MARGIN
        
        new_width = desktop_width - margin * 2
        new_height = work_height - margin * 2
        
        self.animate_to(margin, margin, new_width, new_height)

    def start_move(self, event):
        """Start window dragging."""
        self.focus_window()
        self._x = event.x
        self._y = event.y
        
    def do_move(self, event):
        """Move window during drag."""
        x = self.winfo_x() + event.x - self._x
        y = self.winfo_y() + event.y - self._y
        desktop_width, work_height = self.manager.get_work_area()
        margin = self.manager.WINDOW_MARGIN
        max_x = max(margin, desktop_width - self.winfo_width() - margin)
        max_y = max(margin, work_height - self.winfo_height() - margin)
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
        self.state_file = "window_state.json"
        self.window_states = {}
        self._load_window_states()

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

            window.lift()

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

            window.lift()

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

        self.restore_window_state(title, window)

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

    # =====================================================

    def snap_window(self, window, direction: str):
        """Snap window to screen edge."""
        desktop_width, work_height = self.get_work_area()
        margin = self.WINDOW_MARGIN
        
        if direction == "left":
            new_x = margin
            new_y = margin
            new_width = desktop_width // 2 - margin
            new_height = work_height - margin * 2
        elif direction == "right":
            new_x = desktop_width // 2
            new_y = margin
            new_width = desktop_width // 2 - margin
            new_height = work_height - margin * 2
        elif direction == "top":
            new_x = margin
            new_y = margin
            new_width = desktop_width - margin * 2
            new_height = work_height // 2 - margin
        elif direction == "bottom":
            new_x = margin
            new_y = work_height // 2
            new_width = desktop_width - margin * 2
            new_height = work_height // 2 - margin
        elif direction == "maximize":
            new_x = margin
            new_y = margin
            new_width = desktop_width - margin * 2
            new_height = work_height - margin * 2
        else:
            return
            
        window.animate_to(new_x, new_y, new_width, new_height)

    def _load_window_states(self):
        """Load window states from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    self.window_states = json.load(f)
            except Exception as e:
                print(f"[WindowManager] Error loading states: {e}")
                self.window_states = {}

    def _save_window_states(self):
        """Save window states to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.window_states, f, indent=2)
        except Exception as e:
            print(f"[WindowManager] Error saving states: {e}")

    def save_window_state(self, app_name, window):
        """Save state of a specific window."""
        self.window_states[app_name] = {
            'x': window.winfo_x(),
            'y': window.winfo_y(),
            'width': window.winfo_width(),
            'height': window.winfo_height(),
            'maximized': window.is_maximized,
            'minimized': window.is_minimized
        }
        self._save_window_states()

    def restore_window_state(self, app_name, window):
        """Restore state of a specific window."""
        if app_name in self.window_states:
            state = self.window_states[app_name]
            window.place(x=state['x'], y=state['y'])
            window.configure(width=state['width'], height=state['height'])
            
            if state.get('maximized'):
                window.maximize()
            elif state.get('minimized'):
                window.minimize()