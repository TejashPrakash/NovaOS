from ai.skills.base import Skill, string_parameters
from ai.skills.base import SkillError


def play_music(kernel, song_name: str = "") -> str:
    """Play music (resume or specific song)."""
    try:
        audio_service = kernel.get_service("audio")
        if audio_service:
            if song_name:
                return f"Playing: {song_name}"
            return "Music resumed"
        raise SkillError("Audio service not available")
    except Exception as e:
        raise SkillError(f"Could not play music: {e}")


def pause_music(kernel) -> str:
    """Pause music playback."""
    try:
        audio_service = kernel.get_service("audio")
        if audio_service:
            return "Music paused"
        raise SkillError("Audio service not available")
    except Exception as e:
        raise SkillError(f"Could not pause music: {e}")


def stop_music(kernel) -> str:
    """Stop music playback."""
    try:
        audio_service = kernel.get_service("audio")
        if audio_service:
            return "Music stopped"
        raise SkillError("Audio service not available")
    except Exception as e:
        raise SkillError(f"Could not stop music: {e}")


def next_track(kernel) -> str:
    """Skip to next track."""
    try:
        audio_service = kernel.get_service("audio")
        if audio_service:
            return "Skipped to next track"
        raise SkillError("Audio service not available")
    except Exception as e:
        raise SkillError(f"Could not skip track: {e}")


def previous_track(kernel) -> str:
    """Go to previous track."""
    try:
        audio_service = kernel.get_service("audio")
        if audio_service:
            return "Went to previous track"
        raise SkillError("Audio service not available")
    except Exception as e:
        raise SkillError(f"Could not go to previous track: {e}")


SKILLS = (
    Skill(
        tool=string_parameters(
            name="play_music",
            description="Play music (resume or specific song)",
            song_name="Optional song name to play"
        ),
        run=play_music
    ),
    Skill(
        tool=string_parameters(
            name="pause_music",
            description="Pause music playback"
        ),
        run=pause_music
    ),
    Skill(
        tool=string_parameters(
            name="stop_music",
            description="Stop music playback"
        ),
        run=stop_music
    ),
    Skill(
        tool=string_parameters(
            name="next_track",
            description="Skip to next track"
        ),
        run=next_track
    ),
    Skill(
        tool=string_parameters(
            name="previous_track",
            description="Go to previous track"
        ),
        run=previous_track
    ),
)