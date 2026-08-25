"""Settings service for NovaOS — persists user preferences to disk."""

import json
from pathlib import Path


SETTINGS_FILE = Path(__file__).resolve().parent.parent / "data" / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "cyberpunk",
    "font_size": 14,
    "wallpaper_color": "theme",
    "wallpaper_path": "",
    "volume": 0.7,
    "show_clock": True,
    "show_notifications": True,
    "auto_start_ai": True,
    "ai_provider": "gemini",
    "accent_color": "#00E5FF",
}


class SettingsService:
    """Persistent key-value settings store backed by a JSON file."""

    def __init__(self):
        self.name = "settings"
        self._settings = dict(DEFAULT_SETTINGS)
        self._load()

    # ------------------------------------------------------------------ public API
    def get(self, key: str, default=None):
        """Get a setting by key."""
        return self._settings.get(key, default)

    def set(self, key: str, value):
        """Set a setting and persist to disk."""
        self._settings[key] = value
        self._save()

    def get_all(self) -> dict:
        """Return a copy of all settings."""
        return dict(self._settings)

    def reset(self, key: str = None):
        """Reset one or all settings to defaults."""
        if key:
            self._settings[key] = DEFAULT_SETTINGS.get(key)
        else:
            self._settings = dict(DEFAULT_SETTINGS)
        self._save()

    # ------------------------------------------------------------------ persistence
    def _load(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                self._settings.update(data)
        except Exception as e:
            print(f"[Settings] Could not load settings: {e}")

    def _save(self):
        try:
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"[Settings] Could not save settings: {e}")
