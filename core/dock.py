import customtkinter as ctk
from core.start_menu import StartMenu
from widgets.clock import Clock
from widgets.glass import GlassFrame

class Dock:

    def __init__(self, root):
        self.root = root

        # ==========================================
        # Floating Dock Container
        # ==========================================
        self.frame = GlassFrame(
            self.root,
            width=700,
            height=100,
            blur_amount=20,
            opacity=0.9,
            corner_radius=40,
            border_width=2,
            border_color="#00E5FF40"
        )
        self.frame.place(
            relx=0.5,
            rely=0.93,
            anchor="s"
        )
        self.frame.pack_propagate(False)

        # ==========================================
        # Left Side (Launcher)  
        # ==========================================
        self.left_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.left_frame.pack(
            side="left",
            padx=20,
            fill="y"
        )

        self.launcher_btn = ctk.CTkButton(
            self.left_frame,
            text="✦",
            width=50,
            height=50,
            corner_radius=25,
            fg_color="#00E5FF",
            hover_color="#00FFFF",
            font=("Segoe UI", 24, "bold"),
            command=self.open_launcher,
            border_width=2,
            border_color="#00E5FF80"
        )
        self.launcher_btn.pack(
            pady=25
        )

        # ==========================================
        # Center (Running Apps) - Glass Effect
        # ==========================================
        self.apps_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.apps_frame.pack(
            side="left",
            expand=True,
            fill="both"
        )

        # ==========================================
        # Right Side (Clock) 
        # ==========================================
        self.right_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.right_frame.pack(
            side="right",
            padx=20,
            fill="y"
        )

        self.clock = Clock(self.right_frame)

        # ==========================================
        # Running Apps
        # ==========================================
        self.running_apps = {}

        # ==========================================
        # Launcher (attached later by NovaOS)
        # ==========================================
        self.launcher = None
        self.start_menu = None
        self.start_menu_btn = None

    # =========================================================

    def add_app(self, name, callback):

        if name in self.running_apps:
            return

        button = ctk.CTkButton(
            self.apps_frame,
            text=name,
            width=110,
            height=42,
            corner_radius=20,
            fg_color="#252B3B",
            hover_color="#3A4256",
            command=callback
        )

        button.pack(
            side="left",
            padx=8,
            pady=24
        )

        self.running_apps[name] = button

    # =========================================================

    def remove_app(self, name):

        if name not in self.running_apps:
            return

        self.running_apps[name].destroy()

        del self.running_apps[name]

    # =========================================================

    def open_launcher(self):

        if self.launcher:

            self.launcher.toggle()

    def set_launcher(self, launcher):

        self.launcher = launcher

    # =========================================================

    def add_start_button(self, start_menu=None):
        """Add start button to dock (optional alternative to launcher)."""
        self.start_menu = start_menu  # Store reference to actual start menu

        self.start_menu_btn = ctk.CTkButton(
            self.left_frame,
            text="◈",
            width=45,
            height=45,
            corner_radius=22,
            fg_color="#00E5FF",
            hover_color="#00BCD4",
            font=("Segoe UI", 18, "bold"),
            command=self.toggle_start_menu
        )
        # Replace or add alongside launcher button
        self.launcher_btn.pack_forget()
        self.start_menu_btn.pack(pady=12)

    # =========================================================

    def toggle_start_menu(self):
        """Toggle start menu visibility."""
        if self.start_menu is None:
            print("Open start menu - needs reference to NovaOS start_menu")
        else:
            if self.start_menu.winfo_ismapped():
                self.start_menu.hide()
            else:
                self.start_menu.show()