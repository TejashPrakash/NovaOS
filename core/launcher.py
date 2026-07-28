import customtkinter as ctk


class Launcher:

    def __init__(self, root, window_manager):

        self.root = root
        self.window_manager = window_manager

        self.visible = False

        # -----------------------------
        # Launcher Window
        # -----------------------------

        self.frame = ctk.CTkFrame(
            self.root,
            width=500,
            height=500,
            fg_color="#1A1F2B",
            corner_radius=20,
            border_width=1,
            border_color="#2F3545"
        )

        # -----------------------------
        # Search Box
        # -----------------------------

        self.search = ctk.CTkEntry(
            self.frame,
            placeholder_text="Search applications...",
            height=45
        )

        self.search.pack(
            padx=20,
            pady=(20, 15),
            fill="x"
        )

        self.search.bind(
            "<KeyRelease>",
            self.filter_apps
        )

        # -----------------------------
        # Escape closes launcher
        # -----------------------------

        self.frame.bind("<Escape>", lambda e: self.hide())
        self.search.bind("<Escape>", lambda e: self.hide())

        # -----------------------------
        # Apps Container
        # -----------------------------

        self.apps_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent"
        )

        self.apps_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # -----------------------------
        # Available Apps
        # -----------------------------

        self.apps = [
            ("🌐", "Browser"),
            ("📝", "Notes"),
            ("🧮", "Calculator"),
            ("📁", "Files"),
            ("⚙", "Settings")
        ]

        self.buttons = []

        self.build_apps()

    # ========================================

    def build_apps(self):

        for button in self.buttons:
            button.destroy()

        self.buttons.clear()

        for icon, app in self.apps:

            btn = ctk.CTkButton(
                self.apps_frame,
                text=f"{icon}   {app}",
                height=45,
                anchor="w",
                command=lambda a=app: self.launch(a)
            )

            btn.pack(
                fill="x",
                pady=5
            )

            self.buttons.append(btn)

    # ========================================

    def filter_apps(self, event=None):

        query = self.search.get().lower()

        for button in self.buttons:

            text = button.cget("text").lower()

            if query in text:

                button.pack(fill="x", pady=5)

            else:

                button.pack_forget()
                
    # ========================================

    def launch(self, app):

        self.window_manager.create_window(app)

        self.hide()

    # ========================================

    def show(self):

        if self.visible:
            return

        self.visible = True

        self.frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.search.focus()

    # ========================================

    def hide(self):

        self.visible = False

        self.frame.place_forget()

        self.search.delete(0, "end")

        self.filter_apps()

    # ========================================

    def toggle(self):

        if self.visible:

            self.hide()

        else:

            self.show()