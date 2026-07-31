from dataclasses import dataclass


@dataclass
class BrowserTab:

    id: int

    title: str = "New Tab"

    url: str = "about:home"

    loading: bool = False

    can_go_back: bool = False

    can_go_forward: bool = False