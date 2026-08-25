import threading
from typing import Optional, Callable

try:
    import speech_recognition as sr
    HAS_SR = True
except (ImportError, OSError):
    sr = None
    HAS_SR = False

try:
    import pyttsx3
    HAS_TTS = True
except (ImportError, OSError):
    pyttsx3 = None
    HAS_TTS = False


class VoiceProvider:
    """Voice input/output provider for Nova AI."""

    def __init__(self):
        self.is_listening = False
        self.on_speech_callback: Optional[Callable] = None
        self._listen_thread: Optional[threading.Thread] = None
        self.recognizer = sr.Recognizer() if HAS_SR else None
        self.tts_engine = None

        if HAS_TTS:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.9)
            except Exception:
                self.tts_engine = None

    def start_listening(self, callback: Callable):
        """Start listening for voice commands."""
        if not HAS_SR or self.recognizer is None:
            print("[Voice] speech_recognition not available")
            return
        self.on_speech_callback = callback
        self.is_listening = True
        self._listen_thread = threading.Thread(
            target=self._listen_loop,
            daemon=True,
        )
        self._listen_thread.start()

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
        if self.tts_engine is None:
            return
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"[Voice] TTS error: {e}")

    def set_voice_properties(self, rate: int = None, volume: float = None):
        """Set TTS voice properties."""
        if self.tts_engine is None:
            return
        if rate:
            self.tts_engine.setProperty('rate', rate)
        if volume:
            self.tts_engine.setProperty('volume', volume)