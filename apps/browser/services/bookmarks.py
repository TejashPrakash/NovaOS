import json
from pathlib import Path

DEFAULT_BOOKMARKS = [
    {"title": "Google", "url": "https://www.google.com"},
    {"title": "GitHub", "url": "https://github.com"},
    {"title": "YouTube", "url": "https://youtube.com"},
    {"title": "Wikipedia", "url": "https://wikipedia.org"},
    {"title": "Stack Overflow", "url": "https://stackoverflow.com"}
]

class BookmarkService:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path("data/browser_bookmarks.json")
        self.bookmarks = self._load()

    def _load(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else DEFAULT_BOOKMARKS.copy()
        except (OSError, ValueError):
            return [item.copy() for item in DEFAULT_BOOKMARKS]

    def _save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.bookmarks, indent=2), encoding="utf-8")
        except OSError:
            pass

    def get_all(self):
        return self.bookmarks

    def add(self, title, url):
        bookmark = {"title": title.strip() or url, "url": url.strip()}
        self.bookmarks = [item for item in self.bookmarks if item.get("url") != bookmark["url"]]
        self.bookmarks.append(bookmark)
        self._save()
        return bookmark

    def remove(self, url):
        original_count = len(self.bookmarks)
        self.bookmarks = [item for item in self.bookmarks if item.get("url") != url]
        if len(self.bookmarks) != original_count:
            self._save()
        return len(self.bookmarks) != original_count

    def contains(self, url):
        return any(item.get("url") == url for item in self.bookmarks)