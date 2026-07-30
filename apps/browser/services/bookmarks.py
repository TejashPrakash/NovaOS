DEFAULT_BOOKMARKS = [

    {
        "title": "Google",
        "url": "https://www.google.com"
    },

    {
        "title": "GitHub",
        "url": "https://github.com"
    },

    {
        "title": "YouTube",
        "url": "https://youtube.com"
    },

    {
        "title": "Wikipedia",
        "url": "https://wikipedia.org"
    },

    {
        "title": "Stack Overflow",
        "url": "https://stackoverflow.com"
    }

]


class BookmarkService:

    def __init__(self):

        self.bookmarks = DEFAULT_BOOKMARKS.copy()

    # ==========================================

    def get_all(self):

        return self.bookmarks

    # ==========================================

    def add(self, title, url):

        self.bookmarks.append({

            "title": title,

            "url": url

        })