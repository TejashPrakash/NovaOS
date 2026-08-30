from apps.browser.browser import BrowserApp
from apps.notes.notes import NotesApp
from apps.calculator.calculator import CalculatorApp
from apps.file_manager.file_manager import FileManagerApp
from apps.settings import SettingsApp
from apps.music_player.player import MusicPlayerApp
from apps.terminal.terminal import TerminalApp
from apps.weather.weather import WeatherApp
from apps.system_monitor import SystemMonitorApp
from apps.calendar_app import CalendarApp
from apps.viewer import ViewerApp
from apps.task_manager import TaskManagerApp

APP_REGISTRY = {
    "Browser": BrowserApp,
    "Notes": NotesApp,
    "Calculator": CalculatorApp,
    "Files": FileManagerApp,
    "Settings": SettingsApp,
    "Music Player": MusicPlayerApp,
    "Terminal": TerminalApp,
    "Weather": WeatherApp,
    "System Monitor": SystemMonitorApp,
    "Calendar": CalendarApp,
    "Viewer": ViewerApp,
    "Task Manager": TaskManagerApp,
}