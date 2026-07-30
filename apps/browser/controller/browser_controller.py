class BrowserController:

    HOME_URL = "https://www.google.com"

    def __init__(self):

        self.current_url = self.HOME_URL

        self.back_history = []

        self.forward_history = []

    # =====================================================

    def get_home(self):

        return self.HOME_URL

    # =====================================================

    def get_url(self):

        return self.current_url

    # =====================================================

    def navigate(self, url):

        url = url.strip()

        if not url:
            return self.current_url

        if " " in url:

            url = (
                "https://www.google.com/search?q="
                + url.replace(" ", "+")
            )

        elif not url.startswith("http://") \
                and not url.startswith("https://"):

            url = "https://" + url

        if url != self.current_url:

            self.back_history.append(self.current_url)

            self.forward_history.clear()

            self.current_url = url

        return self.current_url

    # =====================================================

    def go_home(self):

        return self.navigate(self.HOME_URL)

    # =====================================================

    def can_go_back(self):

        return len(self.back_history) > 0

    # =====================================================

    def can_go_forward(self):

        return len(self.forward_history) > 0

    # =====================================================

    def go_back(self):

        if not self.can_go_back():
            return self.current_url

        self.forward_history.append(self.current_url)

        self.current_url = self.back_history.pop()

        return self.current_url

    # =====================================================

    def go_forward(self):

        if not self.can_go_forward():
            return self.current_url

        self.back_history.append(self.current_url)

        self.current_url = self.forward_history.pop()

        return self.current_url