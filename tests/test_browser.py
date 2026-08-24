from apps.browser.controller.browser_controller import BrowserController
from apps.browser.models.tab import BrowserTab
from apps.browser.services.bookmarks import BookmarkService
from apps.browser.services.ai_browser_service import AIBrowserService


def test_controller_normalizes_searches_and_urls():
    controller = BrowserController()
    assert controller.normalize_url("python tkinter") == (
        "https://www.google.com/search?igu=1&q=python+tkinter"
    )
    assert controller.normalize_url("example.com") == "https://example.com"
    assert controller.normalize_url("about:home") == "about:home"


def test_tab_history_truncates_forward_branch():
    controller = BrowserController()
    tab = BrowserTab(1)
    controller.navigate(tab, "one.example")
    controller.navigate(tab, "two.example")
    controller.go_back(tab)
    controller.navigate(tab, "three.example")
    assert tab.history == ["https://one.example", "https://three.example"]
    assert not controller.can_go_forward(tab)


def test_bookmarks_persist_and_deduplicate(tmp_path):
    path = tmp_path / "bookmarks.json"
    service = BookmarkService(path)
    service.add("Nova", "https://nova.example")
    service.add("Nova updated", "https://nova.example")
    reloaded = BookmarkService(path)
    assert reloaded.get_all()[-1] == {
        "title": "Nova updated",
        "url": "https://nova.example",
    }


def test_ai_service_uses_nova_assistant_api():
    class FakeAssistant:
        def ask(self, prompt):
            return f"answered: {prompt}"

    result = AIBrowserService(FakeAssistant()).ask("What matters?")
    assert result.startswith("answered: ")