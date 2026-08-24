from dataclasses import dataclass, field
from typing import List

@dataclass
class BrowserTab:
    id: int
    title: str = "New Tab"
    url: str = "about:home"
    history: List[str] = field(default_factory=list)
    history_index: int = -1
    loading: bool = False
    pinned: bool = False
    last_error: str = ""

    def set_location(self, url: str, title: str = ""):
        self.url = url
        if title:
            self.title = title[:80]