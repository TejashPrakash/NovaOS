from tkinterweb import HtmlFrame


class BrowserWebView:

    def __init__(self, parent):

        self.frame = HtmlFrame(parent)

        # Default Home Page
        self.frame.load_website("https://www.google.com")

    # ---------------------------------------

    def pack(self, **kwargs):

        self.frame.pack(**kwargs)

    # ---------------------------------------

    def load(self, url):

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        self.frame.load_website(url)

    # ---------------------------------------

    def back(self):

        try:
            self.frame.back()
        except:
            pass

    # ---------------------------------------

    def forward(self):

        try:
            self.frame.forward()
        except:
            pass

    # ---------------------------------------

    def reload(self):

        try:
            self.frame.reload()
        except:
            pass