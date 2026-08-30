"""Fully functional Music Player for NovaOS."""

import os
import threading
import time
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
from sdk.app import NovaApp
from core.theme import ThemeManager

try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False

# Supported audio extensions
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"}


class MusicPlayerApp(NovaApp):
    """Fully functional music player with playlist, playback controls, and volume."""

    APP_NAME = "Music Player"
    APP_ICON = "🎵"
    DEFAULT_WIDTH = 650
    DEFAULT_HEIGHT = 520

    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
        self._playlist = []
        self._current_index = -1
        self._is_playing = False
        self._is_paused = False
        self._volume = 0.7
        self._seeking = False
        self._track_length = 0.0
        self._update_job = None

    # ------------------------------------------------------------------ UI
    def build(self):
        # Header
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            header, text="🎵  Music Player",
            font=("Segoe UI", 20, "bold"), text_color="#00E5FF"
        ).pack(side="left")

        # Open folder button
        ctk.CTkButton(
            header, text="📂 Open Folder", width=130, height=32,
            fg_color="#161B22", text_color="#00E5FF",
            hover_color="#1C2333", corner_radius=8,
            border_width=1, border_color="#333333",
            font=("Segoe UI", 12),
            command=self._open_folder
        ).pack(side="right")

        ctk.CTkButton(
            header, text="➕ Add Files", width=110, height=32,
            fg_color="#161B22", text_color="#00E5FF",
            hover_color="#1C2333", corner_radius=8,
            border_width=1, border_color="#333333",
            font=("Segoe UI", 12),
            command=self._add_files
        ).pack(side="right", padx=(0, 8))

        # Now Playing
        self.now_playing_frame = ctk.CTkFrame(
            self.content, fg_color="#161B22", corner_radius=12
        )
        self.now_playing_frame.pack(fill="x", padx=20, pady=(8, 6))

        self.track_title = ctk.CTkLabel(
            self.now_playing_frame, text="No track loaded",
            font=("Segoe UI", 16, "bold"), text_color="#FFFFFF"
        )
        self.track_title.pack(anchor="w", padx=15, pady=(12, 2))

        self.track_artist = ctk.CTkLabel(
            self.now_playing_frame, text="Open a folder or add files to begin",
            font=("Segoe UI", 12), text_color="#888888"
        )
        self.track_artist.pack(anchor="w", padx=15, pady=(0, 8))

        # Progress bar
        self.progress_slider = ctk.CTkSlider(
            self.now_playing_frame, from_=0, to=100,
            width=500, height=14,
            button_color="#00E5FF", button_hover_color="#00C8E8",
            progress_color="#00E5FF", fg_color="#333333",
            command=self._on_seek
        )
        self.progress_slider.pack(fill="x", padx=15, pady=(0, 4))
        self.progress_slider.set(0)

        time_frame = ctk.CTkFrame(self.now_playing_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.time_elapsed = ctk.CTkLabel(
            time_frame, text="0:00", font=("Segoe UI", 11),
            text_color="#888888"
        )
        self.time_elapsed.pack(side="left")

        self.time_total = ctk.CTkLabel(
            time_frame, text="0:00", font=("Segoe UI", 11),
            text_color="#888888"
        )
        self.time_total.pack(side="right")

        # Controls
        ctrl_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        ctrl_frame.pack(pady=(4, 6))

        btn_style = dict(
            width=44, height=44, corner_radius=22,
            fg_color="#161B22", hover_color="#1C2333",
            border_width=1, border_color="#333333",
            font=("Segoe UI Emoji", 18)
        )

        ctk.CTkButton(
            ctrl_frame, text="⏮", text_color="#FFFFFF",
            command=self._prev_track, **btn_style
        ).pack(side="left", padx=6)

        self.play_btn = ctk.CTkButton(
            ctrl_frame, text="▶", text_color="#00E5FF",
            fg_color="#0D1117", hover_color="#1C2333",
            width=56, height=56, corner_radius=28,
            border_width=2, border_color="#00E5FF",
            font=("Segoe UI Emoji", 22),
            command=self._toggle_play
        )
        self.play_btn.pack(side="left", padx=6)

        ctk.CTkButton(
            ctrl_frame, text="⏭", text_color="#FFFFFF",
            command=self._next_track, **btn_style
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            ctrl_frame, text="⏹", text_color="#FF5252",
            command=self._stop, **btn_style
        ).pack(side="left", padx=6)

        # Volume
        vol_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        vol_frame.pack(fill="x", padx=30, pady=(0, 4))

        ctk.CTkLabel(
            vol_frame, text="🔊", font=("Segoe UI Emoji", 14),
            text_color="#888888"
        ).pack(side="left")

        self.volume_slider = ctk.CTkSlider(
            vol_frame, from_=0, to=1, width=150, height=12,
            button_color="#00E5FF", button_hover_color="#00C8E8",
            progress_color="#00E5FF", fg_color="#333333",
            command=self._on_volume_change
        )
        self.volume_slider.pack(side="left", padx=(8, 0))
        self.volume_slider.set(self._volume)

        # Playlist
        playlist_label = ctk.CTkLabel(
            self.content, text="Playlist",
            font=("Segoe UI", 13, "bold"), text_color="#888888"
        )
        playlist_label.pack(anchor="w", padx=20, pady=(6, 2))

        self.playlist_frame = ctk.CTkScrollableFrame(
            self.content, fg_color="#0D1117", corner_radius=8
        )
        self.playlist_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Empty state
        self.empty_label = ctk.CTkLabel(
            self.playlist_frame,
            text="No tracks loaded.\nClick 'Open Folder' or 'Add Files'.",
            font=("Segoe UI", 13), text_color="#555555"
        )
        self.empty_label.pack(pady=40)

    # -------------------------------------------------------------- file ops
    def _open_folder(self):
        folder = filedialog.askdirectory(title="Select Music Folder")
        if not folder:
            return
        self._playlist.clear()
        self._current_index = -1
        self._is_playing = False
        self._is_paused = False

        for root, dirs, files in os.walk(folder):
            for f in sorted(files):
                if Path(f).suffix.lower() in AUDIO_EXTS:
                    self._playlist.append(os.path.join(root, f))

        self._refresh_playlist()
        if self._playlist:
            self._load_track(0)

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma"),
                ("All Files", "*.*")
            ]
        )
        if files:
            for f in files:
                if f not in self._playlist:
                    self._playlist.append(f)
            self._refresh_playlist()
            if self._current_index < 0 and self._playlist:
                self._load_track(0)

    # -------------------------------------------------------------- playlist UI
    def _refresh_playlist(self):
        for w in self.playlist_frame.winfo_children():
            w.destroy()

        if not self._playlist:
            self.empty_label = ctk.CTkLabel(
                self.playlist_frame,
                text="No tracks loaded.\nClick 'Open Folder' or 'Add Files'.",
                font=("Segoe UI", 13), text_color="#555555"
            )
            self.empty_label.pack(pady=40)
            return

        for i, path in enumerate(self._playlist):
            name = Path(path).stem
            row_bg = "#0D2833" if i == self._current_index else "transparent"
            row = ctk.CTkFrame(
                self.playlist_frame, fg_color=row_bg,
                corner_radius=6, height=36
            )
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)

            num_label = ctk.CTkLabel(
                row, text=f" {i + 1:2d}", width=30,
                font=("Segoe UI", 12), text_color="#555555"
            )
            num_label.pack(side="left")

            name_label = ctk.CTkLabel(
                row, text=name, anchor="w",
                font=("Segoe UI", 12),
                text_color="#00E5FF" if i == self._current_index else "#CCCCCC"
            )
            name_label.pack(side="left", fill="x", expand=True)

            # Click to play
            for widget in (row, num_label, name_label):
                widget.bind("<Button-1>", lambda e, idx=i: self._play_index(idx))

    # -------------------------------------------------------------- playback
    def _load_track(self, index):
        if not HAS_PYGAME:
            self.track_title.configure(text="pygame not installed")
            self.track_artist.configure(text="Run: pip install pygame")
            return
        if index < 0 or index >= len(self._playlist):
            return

        self._current_index = index
        path = self._playlist[index]
        name = Path(path).stem

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self._volume)
        except Exception as e:
            self.track_title.configure(text="Error loading track")
            self.track_artist.configure(text=str(e))
            return

        # Try to get track length via mutagen or estimate
        self._track_length = self._estimate_length(path)

        self.track_title.configure(text=name)
        self.track_artist.configure(text=Path(path).parent.name)
        self.time_total.configure(text=self._format_time(self._track_length))
        self.time_elapsed.configure(text="0:00")
        self.progress_slider.set(0)

        self._refresh_playlist()
        self._is_paused = False

    def _estimate_length(self, path):
        """Estimate track length using pygame or file size heuristic."""
        try:
            # pygame doesn't expose length directly, use mutagen if available
            from mutagen.mp3 import MP3
            audio = MP3(path)
            return audio.info.length
        except Exception:
            pass
        try:
            from mutagen.oggvorbis import OggVorbis
            audio = OggVorbis(path)
            return audio.info.length
        except Exception:
            pass
        try:
            from mutagen.flac import FLAC
            audio = FLAC(path)
            return audio.info.length
        except Exception:
            pass
        # Fallback: estimate from file size (rough mp3: 128kbps)
        try:
            size = os.path.getsize(path)
            return size / (128 * 1024 / 8)
        except Exception:
            return 0.0

    def _play_index(self, index):
        self._load_track(index)
        self._play()

    def _play(self):
        if not HAS_PYGAME or self._current_index < 0:
            return
        pygame.mixer.music.play()
        self._is_playing = True
        self._is_paused = False
        self.play_btn.configure(text="⏸")
        self._start_progress_updates()

    def _toggle_play(self):
        if not HAS_PYGAME:
            return
        if self._is_playing and not self._is_paused:
            pygame.mixer.music.pause()
            self._is_paused = True
            self.play_btn.configure(text="▶")
        elif self._is_paused:
            pygame.mixer.music.unpause()
            self._is_paused = False
            self.play_btn.configure(text="⏸")
        elif self._playlist:
            if self._current_index < 0:
                self._load_track(0)
            self._play()

    def _stop(self):
        if not HAS_PYGAME:
            return
        pygame.mixer.music.stop()
        self._is_playing = False
        self._is_paused = False
        self.play_btn.configure(text="▶")
        self.progress_slider.set(0)
        self.time_elapsed.configure(text="0:00")
        self._stop_progress_updates()

    def _prev_track(self):
        if not self._playlist:
            return
        idx = self._current_index - 1
        if idx < 0:
            idx = len(self._playlist) - 1
        self._load_track(idx)
        if self._is_playing:
            self._play()

    def _next_track(self):
        if not self._playlist:
            return
        idx = (self._current_index + 1) % len(self._playlist)
        self._load_track(idx)
        if self._is_playing:
            self._play()

    # -------------------------------------------------------------- volume
    def _on_volume_change(self, value):
        self._volume = value
        if HAS_PYGAME:
            pygame.mixer.music.set_volume(value)

    # -------------------------------------------------------------- seek
    def _on_seek(self, value):
        """Seek to position in track based on slider value (0.0–1.0)."""
        if not self._is_playing or self._track_length <= 0 or not HAS_PYGAME:
            return
        try:
            target_pos = float(value) * self._track_length
            pygame.mixer.music.play(start=target_pos)
            pygame.mixer.music.set_volume(self._volume)
            if self._is_paused:
                pygame.mixer.music.pause()
        except Exception:
            pass

    # -------------------------------------------------------------- progress
    def _start_progress_updates(self):
        self._stop_progress_updates()
        self._update_progress()

    def _stop_progress_updates(self):
        if self._update_job is not None:
            try:
                self.after_cancel(self._update_job)
            except Exception:
                pass
            self._update_job = None

    def _update_progress(self):
        if not self._is_playing or self._is_paused:
            return
        if not HAS_PYGAME:
            return

        # Check if music still playing
        if not pygame.mixer.music.get_busy():
            # Track ended — auto next
            self._next_track()
            if self._current_index >= 0:
                self._play()
            return

        # Update elapsed time display
        # pygame doesn't expose position, so we track it ourselves
        try:
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms < 0:
                pos_ms = 0
            pos_sec = pos_ms / 1000.0
            self.time_elapsed.configure(text=self._format_time(pos_sec))

            if self._track_length > 0:
                pct = min(pos_sec / self._track_length, 1.0)
                self.progress_slider.set(pct)
        except Exception:
            pass

        self._update_job = self.after(500, self._update_progress)

    # -------------------------------------------------------------- helpers
    @staticmethod
    def _format_time(seconds):
        if seconds < 0:
            seconds = 0
        m = int(seconds) // 60
        s = int(seconds) % 60
        return f"{m}:{s:02d}"

    # -------------------------------------------------------------- cleanup
    def destroy(self):
        self._stop_progress_updates()
        if HAS_PYGAME:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        super().destroy()
