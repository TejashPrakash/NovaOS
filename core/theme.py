from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class ColorScheme:
    """Premium color scheme for NovaOS."""
    
    # Primary colors
    primary: str = "#00E5FF"  # Cyan neon
    primary_dim: str = "#00B8D4"  # Dimmed cyan
    secondary: str = "#7B61FF"  # Purple neon
    accent: str = "#FF00E5"  # Magenta neon
    
    # Background colors
    background: str = "#0A0E14"  # Deep dark
    surface: str = "#161B22"  # Surface dark
    surface_light: str = "#1F242E"  # Lighter surface
    
    # Text colors
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#BBBBBB"
    text_muted: str = "#666666"
    
    # Glow effects
    glow_primary: str = "#00E5FF"
    glow_secondary: str = "#7B61FF"
    glow_accent: str = "#FF00E5"
    
    # Borders
    border_light: str = "#FFFFFF"
    border_primary: str = "#00E5FF"
    
    # Additional hover colors
    primary_hover: str = "#00BCD4"
    secondary_hover: str = "#9D7CFF"
    accent_hover: str = "#FF66E5"
    
    # Status colors
    success: str = "#00E676"
    warning: str = "#FFC107"
    error: str = "#E53935"
    info: str = "#00E5FF"
    
    # Surface variants
    surface_lighter: str = "#252B3B"
    
    @classmethod
    def get_gradient(cls, color1: str, color2: str, steps: int = 10) -> list:
        """Generate gradient between two colors."""
        colors = []
        for i in range(steps):
            ratio = i / (steps - 1)
            colors.append(ColorScheme._interpolate_color(color1, color2, ratio))
        return colors
        
    @staticmethod
    def _interpolate_color(color1: str, color2: str, ratio: float) -> str:
        """Interpolate between two hex colors."""
        c1 = ColorScheme._hex_to_rgb(color1)
        c2 = ColorScheme._hex_to_rgb(color2)
        
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        
        return f"#{r:02x}{g:02x}{b:02x}"
        
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB."""
        hex_color = hex_color.lstrip('#')
        rgb_values = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return rgb_values[0], rgb_values[1], rgb_values[2]


class ThemeManager:
    """Manage NovaOS premium theme."""
    
    def __init__(self):
        self.color_scheme = ColorScheme()
        self.current_theme = "cyberpunk"
        
    def get_color(self, color_name: str) -> str:
        """Get color from current scheme."""
        return getattr(self.color_scheme, color_name, "#FFFFFF")

    def get_current_theme(self) -> str:
        """Return the name of the active theme."""
        return self.current_theme
        
    def apply_theme(self, theme_name: str):
        """Apply a specific theme with enhanced color schemes."""
        self.current_theme = theme_name
        if theme_name == "cyberpunk":
            self.color_scheme = ColorScheme()
        elif theme_name == "neon":
            self.color_scheme = ColorScheme(
                primary="#FF00FF",
                primary_hover="#FF66FF",
                secondary="#00FFFF",
                secondary_hover="#00CCFF",
                accent="#FFFF00",
                accent_hover="#FFFF66"
            )
        elif theme_name == "sunset":
            self.color_scheme = ColorScheme(
                primary="#FF6B35",
                primary_hover="#FF8C5A",
                secondary="#F7C59F",
                secondary_hover="#FFE0B2",
                accent="#FF006E",
                accent_hover="#FF3385"
            )
        elif theme_name == "ocean":
            self.color_scheme = ColorScheme(
                primary="#00D4FF",
                primary_hover="#00A8CC",
                secondary="#0066FF",
                secondary_hover="#0088FF",
                accent="#00FF99",
                accent_hover="#00FFBB"
            )