class BrowserController:

    HOME_URL = "https://www.google.com"

    # ============================================

    def normalize_url(self, url):

        url = url.strip()

        if not url:
            return self.HOME_URL

        if " " in url:

            return (
                "https://www.google.com/search?q="
                + url.replace(" ", "+")
            )

        if not url.startswith("http://") \
                and not url.startswith("https://"):

            return "https://" + url

        return url

    # ============================================

    def navigate(self, tab, url):

        url = self.normalize_url(url)

        if tab.history_index < len(tab.history) - 1:
            tab.history = tab.history[:tab.history_index + 1]

        if not tab.history or tab.history[-1] != url:
            tab.history.append(url)

        tab.history_index = len(tab.history) - 1
        tab.url = url

        return url

    # ============================================

    def go_home(self, tab):

        return self.navigate(tab, self.HOME_URL)

    # ============================================

    def can_go_back(self, tab):

        return tab.history_index > 0

    # ============================================

    def can_go_forward(self, tab):

        return tab.history_index < len(tab.history) - 1

    # ============================================

    def go_back(self, tab):

        if not self.can_go_back(tab):
            return tab.url

        tab.history_index -= 1

        tab.url = tab.history[tab.history_index]

        return tab.url

    # ============================================

    def go_forward(self, tab):

        if not self.can_go_forward(tab):
            return tab.url

        tab.history_index += 1

        tab.url = tab.history[tab.history_index]

        return tab.url