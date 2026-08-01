from dataclasses import dataclass, field


@dataclass
class BrowserTab:

    id: int

    title: str = "New Tab"

    url: str = "about:home"

    history: list = field(default_factory=list)

    history_index: int = -1

    loading: bool = False