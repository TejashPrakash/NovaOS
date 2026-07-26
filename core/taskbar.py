import customtkinter as ctk
from widgets.clock import Clock


class Taskbar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            height=48,
            fg_color="#111827",
            corner_radius=0
        )

        self.pack(
            side="bottom",
            fill="x"
        )

        # =====================================
        # Start Button
        # =====================================

        self.start_button = ctk.CTkButton(
            self,
            text="⊞ Nova",
            width=90
        )

        self.start_button.pack(
            side="left",
            padx=10,
            pady=6
        )

        # =====================================
        # Running Apps Area
        # =====================================

        self.apps_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.apps_frame.pack(
            side="left",
            padx=10
        )

        self.app_buttons = {}

        # =====================================
        # Clock
        # =====================================

        self.clock = Clock(self)

        self.clock.pack(
            side="right",
            padx=15
        )

    # =====================================
    # Add App
    # =====================================

    def add_app(self, window):

        button = ctk.CTkButton(
            self.apps_frame,
            text=window.title,
            width=110,
            command=window.focus
        )

        button.pack(
            side="left",
            padx=4
        )

        self.app_buttons[window] = button

    # =====================================
    # Remove App
    # =====================================

    def remove_app(self, window):

        if window in self.app_buttons:

            self.app_buttons[window].destroy()

            del self.app_buttons[window]