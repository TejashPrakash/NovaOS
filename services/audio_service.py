"""Audio service for NovaOS — manages system sounds and notification audio."""

import os
from pathlib import Path

try:
    import pygame
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False

SOUNDS_DIR = Path(__file__).resolve().parent.parent / "assets" / "sounds"

# Built-in system sound events
SOUND_EVENTS = {
    "notification": "notification.wav",
    "startup": "startup.wav",
    "shutdown": "shutdown.wav",
    "error": "error.wav",
    "click": "click.wav",
}


class AudioService:
    """Manages system sounds, volume, and audio playback."""

    def __init__(self):
        self.name = "audio"
        self._volume = 0.7
        self._muted = False
        self._enabled = HAS_PYGAME
        SOUNDS_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ public API
    def play_sound(self, event_name: str):
        """Play a system sound by event name (e.g. 'notification', 'startup')."""
        if not self._enabled or self._muted:
            return

        filename = SOUND_EVENTS.get(event_name)
        if not filename:
            print(f"[Audio] Unknown sound event: {event_name}")
            return

        sound_path = SOUNDS_DIR / filename
        if not sound_path.exists():
            # Sound file not installed — silent fallback
            return

        try:
            sound = pygame.mixer.Sound(str(sound_path))
            sound.set_volume(self._volume)
            sound.play()
        except Exception as e:
            print(f"[Audio] Could not play {event_name}: {e}")

    def play_file(self, file_path: str):
        """Play an arbitrary audio file."""
        if not self._enabled or self._muted:
            return
        if not os.path.isfile(file_path):
            print(f"[Audio] File not found: {file_path}")
            return
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(self._volume)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"[Audio] Could not play file: {e}")

    def stop(self):
        """Stop any currently playing audio."""
        if self._enabled:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

    def set_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, volume))
        if self._enabled:
            try:
                pygame.mixer.music.set_volume(self._volume)
            except Exception:
                pass

    def get_volume(self) -> float:
        return self._volume

    def mute(self):
        self._muted = True
        self.stop()

    def unmute(self):
        self._muted = False

    def toggle_mute(self):
        if self._muted:
            self.unmute()
        else:
            self.mute()
        return self._muted

    def is_muted(self) -> bool:
        return self._muted

    def is_available(self) -> bool:
        return self._enabled
