"""Wallpaper service for NovaOS — manages desktop background images and colors."""

import os
from pathlib import Path


WALLPAPER_DIR = Path(__file__).resolve().parent.parent / "assets" / "wallpapers"

PRESET_COLORS = {
    "cyberpunk": "#0D1117",
    "midnight": "#0a0e1a",
    "ocean": "#0b1628",
    "forest": "#0b1a0f",
    "sunset": "#1a0b0b",
    "arctic": "#0f1a2e",
    "default": "#0D1117",
}


class WallpaperService:
    """Manages desktop background images and solid-color wallpapers."""

    def __init__(self):
        self.name = "wallpaper"
        self._current_path = ""
        self._current_color = PRESET_COLORS["default"]
        self._on_change_callback = None

    # ------------------------------------------------------------------ public API
    def set_color(self, color_name_or_hex: str):
        """Set wallpaper to a preset name or a hex color string."""
        if color_name_or_hex in PRESET_COLORS:
            self._current_color = PRESET_COLORS[color_name_or_hex]
        else:
            self._current_color = color_name_or_hex
        self._current_path = ""
        self._notify()

    def set_image(self, image_path: str):
        """Set wallpaper to an image file."""
        if os.path.isfile(image_path):
            self._current_path = image_path
            self._notify()
        else:
            print(f"[Wallpaper] File not found: {image_path}")

    def get_current(self) -> dict:
        """Return current wallpaper state."""
        return {
            "type": "image" if self._current_path else "color",
            "path": self._current_path,
            "color": self._current_color,
        }

    def list_available(self) -> list:
        """List available wallpaper images in the assets folder."""
        WALLPAPER_DIR.mkdir(parents=True, exist_ok=True)
        exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
        return sorted(
            str(f) for f in WALLPAPER_DIR.iterdir()
            if f.suffix.lower() in exts
        ) if WALLPAPER_DIR.exists() else []

    def list_presets(self) -> dict:
        """Return available color presets."""
        return dict(PRESET_COLORS)

    def on_change(self, callback):
        """Register a callback for when the wallpaper changes."""
        self._on_change_callback = callback

    # ------------------------------------------------------------------ internal
    def _notify(self):
        if self._on_change_callback:
            try:
                self._on_change_callback(self.get_current())
            except Exception as e:
                print(f"[Wallpaper] Callback error: {e}")
