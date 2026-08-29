import customtkinter as ctk
import tkinter as tk
from ai.ui.panel import AIPanel
from PIL import Image, ImageTk
import os
from core.theme import ThemeManager
from core.ai_background import ensure_wallpaper


class Desktop:
    """NovaOS Desktop — single-layer architecture.
    All widgets (icons, AI features, tray) live directly on self.frame.
    Wallpaper is a Canvas behind everything on the frame.
    """

    def __init__(self, root):
        self.root = root
        self.background_image = None
        self.theme = ThemeManager()
        self.ai_panel = None
        self._wallpaper_path = None
        self.neural_background = None
        self.ai_bg = None
        self.ambient_lighting = None

        # Main Desktop Frame (THE ONE AND ONLY LAYER)
        self.frame = ctk.CTkFrame(
            self.root,
            fg_color="#0D1117",
            corner_radius=0
        )
        self.frame.pack(fill="both", expand=True)

        # Wallpaper Canvas (Tkinter Canvas — reliable image display)
        self.wallpaper_canvas = tk.Canvas(
            self.frame, highlightthickness=0, bg="#0D1117"
        )
        self.wallpaper_canvas.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        self._bg_photo = None  # prevent GC

        # Load wallpaper after window is fully rendered
        # Use Configure event for reliable sizing
        self.frame.bind("<Configure>", self._on_frame_configure)
        self._wallpaper_loaded = False
        self.frame.after(800, self._load_wallpaper)
        self.frame.after(1500, self._load_wallpaper)
        self.frame.after(3000, self._load_wallpaper)

    def _on_frame_configure(self, event=None):
        """Re-load wallpaper when frame resizes."""
        if self._wallpaper_loaded and self._wallpaper_path:
            self.set_background_image(self._wallpaper_path)

    def _load_wallpaper(self):
        """Load and display AI wallpaper on canvas."""
        if self._wallpaper_loaded:
            return
        try:
            self._wallpaper_path = ensure_wallpaper()
            self.set_background_image(self._wallpaper_path)
            self._wallpaper_loaded = True
        except Exception as e:
            print(f"[Desktop] AI wallpaper failed: {e}")
            import traceback
            traceback.print_exc()

    def set_background_image(self, image_path):
        """Set background image on canvas."""
        try:
            if not os.path.exists(image_path):
                return
            image = Image.open(image_path)
            # Use frame dimensions (more reliable than screen during init)
            fw = self.frame.winfo_width()
            fh = self.frame.winfo_height()
            w = fw if fw > 100 else self.root.winfo_screenwidth()
            h = fh if fh > 100 else self.root.winfo_screenheight()
            if w < 100:
                w, h = 1920, 1080
            image = image.resize((w, h), Image.Resampling.LANCZOS)
            self._bg_photo = ImageTk.PhotoImage(image)
            self.wallpaper_canvas.delete("all")
            # Update canvas size to match
            self.wallpaper_canvas.configure(width=w, height=h)
            self.wallpaper_canvas.create_image(0, 0, anchor="nw", image=self._bg_photo)
            # Canvas is already at the bottom (first child created)
            # No need to call lower() which requires a tag argument
        except Exception as e:
            print(f"[Desktop] Error loading background: {e}")

    def set_background_color(self, color):
        """Set solid background color."""
        c = self.theme.get_color("background") if color == "theme" else color
        self.wallpaper_canvas.configure(bg=c)

    def enable_neural_network_background(self):
        from widgets.neural_background import NeuralBackground
        if self.neural_background is None:
            self.neural_background = NeuralBackground(self.frame)
            self.neural_background.place(relwidth=1, relheight=1)
            # Lower neural_background behind wallpaper in the parent frame's z-order
            self.frame.lower(self.neural_background)

    def disable_neural_network_background(self):
        if self.neural_background:
            self.neural_background.destroy()
            self.neural_background = None

    def enable_ambient_lighting(self):
        from widgets.ambient_lighting import AmbientLighting
        if self.ambient_lighting is None:
            self.ambient_lighting = AmbientLighting(self.frame)
            self.ambient_lighting.place(relwidth=1, relheight=1)

    def disable_ambient_lighting(self):
        if self.ambient_lighting:
            self.ambient_lighting.destroy()
            self.ambient_lighting = None

    # Public API — all return self.frame (single layer)
    def get_canvas(self):
        return self.frame

    def get_widget_layer(self):
        return self.frame

    def get_icon_layer(self):
        return self.frame

    def toggle_ai_panel(self, assistant):
        if self.ai_panel is None:
            self.ai_panel = AIPanel(self.frame, assistant)
            self.ai_panel.place(relx=0.5, rely=0.5, anchor="center")
            self.ai_panel.lift()
        else:
            self.ai_panel.destroy()
            self.ai_panel = None

    def set_theme(self, theme_name: str):
        self.theme.apply_theme(theme_name)
        if self._wallpaper_path and os.path.exists(self._wallpaper_path):
            self.set_background_image(self._wallpaper_path)
        else:
            self.set_background_color("theme")
        if self.neural_background:
            self.disable_neural_network_background()
            self.enable_neural_network_background()
        if self.ambient_lighting:
            self.disable_ambient_lighting()
            self.enable_ambient_lighting()

    def get_theme_manager(self):
        return self.theme
