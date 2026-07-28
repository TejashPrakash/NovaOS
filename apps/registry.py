from apps.browser import BrowserApp
from apps.notes import NotesApp
from apps.calculator import CalculatorApp
from apps.file_manager import FileManagerApp
from apps.settings import SettingsApp
from apps.music_player import MusicPlayerApp

APP_REGISTRY = {

    "Browser": BrowserApp,

    "Notes": NotesApp,

    "Calculator": CalculatorApp,

    "Files": FileManagerApp,

    "Settings": SettingsApp,

    "Music Player": MusicPlayerApp
}