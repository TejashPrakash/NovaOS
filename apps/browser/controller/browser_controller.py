class BrowserController:
    HOME_URL = "https://www.google.com"
    
    def normalize_url(self, url):
        if not url:
            return self.HOME_URL
        url = url.strip()
        if " " in url:
            return (
                "https://www.google.com/search?q="
                + url.replace(" ", "+")
            )
        if not url.startswith("http://") and not url.startswith("https://"):
            return "https://" + url
        return url
    
    def navigate(self, tab, url):
        if not tab:
            print("[BrowserController] No tab provided for navigation")
            return self.HOME_URL
        url = self.normalize_url(url)
        if tab.history_index < len(tab.history) - 1:
            tab.history = tab.history[:tab.history_index + 1]
        if not tab.history or tab.history[-1] != url:
            tab.history.append(url)
        tab.history_index = len(tab.history) - 1
        tab.url = url
        return url
    
    def go_home(self, tab):
        if not tab:
            print("[BrowserController] No tab provided for home")
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
            print("[BrowserController] No tab provided for back")
            return self.HOME_URL
        if not self.can_go_back(tab):
            return tab.url
        tab.history_index -= 1
        tab.url = tab.history[tab.history_index]
        return tab.url
    
    def go_forward(self, tab):
        if not tab:
            print("[BrowserController] No tab provided for forward")
            return self.HOME_URL
        if not self.can_go_forward(tab):
            return tab.url
        tab.history_index += 1
        tab.url = tab.history[tab.history_index]
        return tab.url