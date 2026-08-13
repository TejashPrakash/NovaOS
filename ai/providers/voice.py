"""Voice input/output provider for NovaOS AI."""

import speech_recognition as sr
import pyttsx3
from typing import Optional, Callable
from .base_provider import BaseProvider


class VoiceProvider:
    """Voice input/output provider for Nova AI."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.is_listening = False
        self.on_speech_callback: Optional[Callable] = None

        # Configure TTS
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)

    def start_listening(self, callback: Callable):
        """Start listening for voice commands."""
        self.on_speech_callback = callback
        self.is_listening = True
        self._listen_loop()

    def stop_listening(self):
        """Stop listening for voice commands."""
        self.is_listening = False

    def _listen_loop(self):
        """Continuous listening loop."""
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio)

                    if self.on_speech_callback:
                        self.on_speech_callback(text)

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"[Voice] Error: {e}")
                continue

    def speak(self, text: str):
        """Speak text using TTS."""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"[Voice] TTS error: {e}")

    def set_voice_properties(self, rate: int = None, volume: float = None):
        """Set TTS voice properties."""
        if rate:
            self.tts_engine.setProperty('rate', rate)
        if volume:
            self.tts_engine.setProperty('volume', volume)