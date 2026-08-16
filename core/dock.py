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
            height=70,
            blur_amount=20,
            opacity=0.9,
            corner_radius=40,
            border_width=2,
            border_color="#00E5FF"
        )
        self.frame.place(
            relx=0.5,
            rely=0.94,
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
            padx=15,
            fill="y"
        )
        
        self.launcher_btn = ctk.CTkButton(
            self.left_frame,
            text="✦",
            width=45,
            height=45,
            corner_radius=22,
            fg_color="#00E5FF",
            hover_color="#00FFFF",
            font=("Segoe UI", 22, "bold"),
            command=self.open_launcher,
            border_width=2,
            border_color="#00E5FF"
        )
        self.launcher_btn.pack(
            pady=12
        )
        
        # ==========================================
        # Center (Running Apps)
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
            padx=15,
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
            pady=14
        )
        self.running_apps[name] = button
        
    def remove_app(self, name):
        if name not in self.running_apps:
            return
        self.running_apps[name].destroy()
        del self.running_apps[name]
        
    def open_launcher(self):
        if self.launcher:
            self.launcher.toggle()
            
    def set_launcher(self, launcher):
        self.launcher = launcher
        
    def add_start_button(self, start_menu=None):
        """Add start menu reference for integration."""
        self.start_menu = start_menu
        
    def integrate_launcher_with_start_menu(self):
        """Integrate launcher with start menu for dual functionality."""
        if self.start_menu and self.launcher:
            # Store original toggle method
            original_toggle = self.launcher.toggle
            
            def enhanced_toggle():
                # Toggle both launcher and start menu
                original_toggle()
                if self.start_menu.winfo_ismapped():
                    self.start_menu.hide()
                else:
                    self.start_menu.show()
                    
            self.launcher.toggle = enhanced_toggle