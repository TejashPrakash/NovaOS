from urllib.parse import quote_plus, urlparse


class BrowserController:
    HOME_URL = "about:home"
    # igu=1 asks Google for its non-JavaScript search response, which works in
    # tkinterweb's embedded renderer as well as full browser engines.
    SEARCH_URL = "https://www.google.com/search?igu=1&q={}"
    SUPPORTED_SCHEMES = {"http", "https", "about", "file"}

    def normalize_url(self, url):
        if not url:
            return self.HOME_URL
        url = url.strip()
        if " " in url or ("." not in url and ":" not in url):
            return self.SEARCH_URL.format(quote_plus(url))
        parsed = urlparse(url if "://" in url or url.startswith("about:") else "https://" + url)
        if parsed.scheme not in self.SUPPORTED_SCHEMES:
            return self.SEARCH_URL.format(quote_plus(url))
        if parsed.scheme == "about":
            return url
        if not url.startswith(("http://", "https://", "file://")):
            return "https://" + url
        return url

    def navigate(self, tab, url):
        if not tab:
            return self.normalize_url(url)
        url = self.normalize_url(url)
        if tab.history_index < len(tab.history) - 1:
            tab.history = tab.history[:tab.history_index + 1]
        if not tab.history or tab.history[-1] != url:
            tab.history.append(url)
        tab.history_index = len(tab.history) - 1
        tab.set_location(url)
        return url

    def go_home(self, tab):
        if not tab:
            return self.HOME_URL
        return self.navigate(tab, self.HOME_URL)

    def can_go_back(self, tab):
        if not tab:
            return False
        return tab.history_index > 0

    def can_go_forward(self, tab):
        if not tab:
            return False
        return tab.history_index < len(tab.history) - 1

    def go_back(self, tab):
        if not tab:
            return self.HOME_URL
        if not self.can_go_back(tab):
            return tab.url
        tab.history_index -= 1
        tab.url = tab.history[tab.history_index]
        return tab.url

    def go_forward(self, tab):
        if not tab:
            return self.HOME_URL
        if not self.can_go_forward(tab):
            return tab.url
        tab.history_index += 1
        tab.url = tab.history[tab.history_index]
        return tab.url