from pathlib import Path


FILE_ICONS = {

    ".py": "🐍",
    ".txt": "📄",
    ".md": "📝",
    ".pdf": "📕",

    ".png": "🖼",
    ".jpg": "🖼",
    ".jpeg": "🖼",
    ".gif": "🖼",
    ".bmp": "🖼",
    ".webp": "🖼",

    ".mp3": "🎵",
    ".wav": "🎵",
    ".ogg": "🎵",
    ".flac": "🎵",

    ".mp4": "🎬",
    ".avi": "🎬",
    ".mkv": "🎬",
    ".mov": "🎬",

    ".zip": "🗜",
    ".rar": "🗜",
    ".7z": "🗜",

    ".html": "🌐",
    ".css": "🎨",
    ".js": "⚡",
    ".json": "📋",

    ".exe": "⚙",
}


def get_icon(path: Path):

    if path.is_dir():
        return "📁"

    return FILE_ICONS.get(
        path.suffix.lower(),
        "📄"
    )