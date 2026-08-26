"""Sound effects system for NovaOS — generates tones at startup, no external files needed."""

import math
import struct
import wave
import io
import os
from pathlib import Path

try:
    import pygame
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False

SOUNDS_DIR = Path(__file__).resolve().parent.parent / "assets" / "sounds"


def _generate_tone(frequency, duration_ms, volume=0.3, fade_out=True):
    """Generate a sine wave tone and return it as a pygame Sound object."""
    if not HAS_PYGAME:
        return None

    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    n_bytes = n_samples * 2  # 16-bit mono

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            # Envelope: fade in and fade out
            if fade_out:
                envelope = min(1.0, t * 20) * max(0, 1.0 - (t - duration_ms / 2000) * 4)
            else:
                envelope = min(1.0, t * 20)

            value = volume * envelope * math.sin(2 * math.pi * frequency * t)
            sample = int(value * 32767)
            wav.writeframes(struct.pack('<h', max(-32768, min(32767, sample))))

    buf.seek(0)
    try:
        sound = pygame.mixer.Sound(buffer=buf.read())
        return sound
    except Exception:
        return None


def _generate_chord(frequencies, duration_ms, volume=0.2):
    """Generate a chord from multiple frequencies."""
    if not HAS_PYGAME:
        return None

    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)

    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        for i in range(n_samples):
            t = i / sample_rate
            envelope = min(1.0, t * 15) * max(0, 1.0 - t / (duration_ms / 1000))

            value = 0
            for freq in frequencies:
                value += volume * math.sin(2 * math.pi * freq * t)
            value *= envelope / len(frequencies)

            sample = int(value * 32767)
            wav.writeframes(struct.pack('<h', max(-32768, min(32767, sample))))

    buf.seek(0)
    try:
        return pygame.mixer.Sound(buffer=buf.read())
    except Exception:
        return None


class SoundManager:
    """Manages all system sounds for NovaOS."""

    def __init__(self):
        self._sounds = {}
        self._volume = 0.5
        self._enabled = HAS_PYGAME
        self._generate_sounds()

    def _generate_sounds(self):
        """Pre-generate all system sounds."""
        if not self._enabled:
            return

        # Boot sound — pleasant ascending chord
        self._sounds["boot"] = _generate_chord(
            [523, 659, 784],  # C5, E5, G5 major chord
            duration_ms=800, volume=0.25
        )

        # Click — short high tick
        self._sounds["click"] = _generate_tone(
            1200, duration_ms=50, volume=0.15
        )

        # Success — ascending notes
        self._sounds["success"] = _generate_chord(
            [659, 784],  # E5, G5
            duration_ms=300, volume=0.2
        )

        # Error — low buzz
        self._sounds["error"] = _generate_tone(
            200, duration_ms=200, volume=0.2
        )

        # Notification — gentle ping
        self._sounds["notification"] = _generate_tone(
            880,  # A5
            duration_ms=400, volume=0.2
        )

        # Shutdown — descending chord
        self._sounds["shutdown"] = _generate_chord(
            [784, 659, 523],  # G5, E5, C5 descending
            duration_ms=600, volume=0.2
        )

        # Lock — quick lock sound
        self._sounds["lock"] = _generate_tone(
            600,
            duration_ms=150, volume=0.15
        )

        # Unlock — pleasant double ping
        self._sounds["unlock"] = _generate_chord(
            [880, 1100],
            duration_ms=300, volume=0.2
        )

    def play(self, sound_name):
        """Play a named sound effect."""
        if not self._enabled:
            return
        sound = self._sounds.get(sound_name)
        if sound:
            try:
                sound.set_volume(self._volume)
                sound.play()
            except Exception:
                pass

    def set_volume(self, volume):
        """Set master sound volume (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, volume))

    def get_volume(self):
        return self._volume

    def enable(self):
        self._enabled = HAS_PYGAME

    def disable(self):
        self._enabled = False

    def is_available(self):
        return HAS_PYGAME


# Global instance
sound_manager = SoundManager()
