import customtkinter as ctk
from ai.ui.panel import AIPanel
from PIL import Image, ImageTk
import os
from widgets.neural_background import NeuralBackground
from widgets.ambient_lighting import AmbientLighting
from core.theme import ThemeManager
from core.ai_background import AIBackground
class Desktop:
    def __init__(self, root):
        self.root = root
        self.background_image = None
        
        # -----------------------------
        # Main Desktop Area
        # -----------------------------
        self.frame = ctk.CTkFrame(
            self.root,
            fg_color="#0D1117",
            corner_radius=0
        )
        self.frame.pack(
            fill="both",
            expand=True
        )
        
        # -----------------------------
        # Wallpaper Layer
        # -----------------------------
        self.wallpaper = ctk.CTkLabel(
            self.frame,
            text="",
            fg_color="transparent"
        )
        self.wallpaper.place(
            relwidth=1,
            relheight=1
        )

        # Add neural network background option
        self.neural_background = None
        self.theme = ThemeManager()
        self.ai_bg = None
        self._setup_default_background()
        
        # -----------------------------
        # Desktop Widgets Layer (on top of AI background)
        # -----------------------------
        self.widget_layer = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.widget_layer.place(
            relwidth=1,
            relheight=1
        )
        self.widget_layer.lift()
        
        # -----------------------------
        # Desktop Icons Layer
        # -----------------------------
        self.icon_layer = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.icon_layer.place(
            relwidth=1,
            relheight=1
        )
        self.icon_layer.lift()

        # -----------------------------
        # Ambient Lighting Layer (optional)
        # -----------------------------
        self.ambient_lighting = None

        self.ai_panel = None
        
    def _setup_default_background(self):
        """Setup vibrant AI background."""
        try:
            self.ai_bg = AIBackground(self.frame)
            self.ai_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
            # Push background below all other layers
            self.ai_bg.lower(self.wallpaper)
        except Exception as e:
            print(f"[Desktop] AI background failed, using solid: {e}")
            self.wallpaper.configure(fg_color=self.theme.get_color("background"))
        
    def set_background_image(self, image_path):
        """Set background image from file."""
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((2000, 2000), Image.Resampling.LANCZOS)
                self.background_image = ImageTk.PhotoImage(image)
                self.wallpaper.configure(image=self.background_image)
        except Exception as e:
            print(f"[Desktop] Error loading background: {e}")
            
    def set_background_color(self, color):
        """Set solid background color with theme support."""
        if color == "theme":
            self.wallpaper.configure(
                fg_color=self.theme.get_color("background"),
                image=""
            )
        else:
            self.wallpaper.configure(
                fg_color=color,
                image=""
            )

    def enable_neural_network_background(self):
        """Enable animated neural network background."""
        if self.ai_bg:
            try:
                self.ai_bg.destroy()
            except Exception:
                pass
            self.ai_bg = None
        if self.neural_background is None:
            self.neural_background = NeuralBackground(self.wallpaper)
            self.neural_background.place(relwidth=1, relheight=1)

    def disable_neural_network_background(self):
        """Disable neural network background."""
        if self.neural_background:
            self.neural_background.destroy()
            self.neural_background = None

    def enable_ambient_lighting(self):
        """Enable ambient lighting effects."""
        if self.ambient_lighting is None:
            self.ambient_lighting = AmbientLighting(self.widget_layer)
            self.ambient_lighting.place(relwidth=1, relheight=1)

    def disable_ambient_lighting(self):
        """Disable ambient lighting effects."""
        if self.ambient_lighting:
            self.ambient_lighting.destroy()
            self.ambient_lighting = None
        
    # ==========================================
    # Public API
    # ==========================================
    def get_canvas(self):
        return self.frame
        
    def get_widget_layer(self):
        return self.widget_layer
        
    def get_icon_layer(self):
        return self.icon_layer
        
    def toggle_ai_panel(self, assistant):
        """Toggle AI panel visibility."""
        if self.ai_panel is None:
            self.ai_panel = AIPanel(self.get_widget_layer(), assistant)
            self.ai_panel.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.ai_panel.destroy()
            self.ai_panel = None
    
    def set_theme(self, theme_name: str):
        """Apply theme to desktop."""
        self.theme.apply_theme(theme_name)
        self.set_background_color("theme")
        
        # Update existing premium effects if active
        if self.neural_background:
            self.disable_neural_network_background()
            self.enable_neural_network_background()
        
        if self.ambient_lighting:
            self.disable_ambient_lighting()
            self.enable_ambient_lighting()

    def get_theme_manager(self):
        """Get theme manager instance."""
        return self.theme