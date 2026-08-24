import sys

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView


class NovaWebPage(QWebEnginePage):
    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        return True


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "about:blank"
    app = QApplication(sys.argv)
    app.setApplicationName("Nova Browser")

    profile = QWebEngineProfile("NovaBrowser", app)
    profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
    profile.setPersistentStoragePath("data/browser_profile")

    window = QMainWindow()
    window.setWindowTitle("Nova Browser")
    window.resize(1280, 860)

    view = QWebEngineView(window)
    page = NovaWebPage(profile, view)
    view.setPage(page)
    settings = view.settings()
    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
    view.load(QUrl(url))

    def handle_fullscreen(enabled):
        window.showFullScreen() if enabled else window.showNormal()

    page.fullScreenRequested.connect(lambda request: (request.accept(), handle_fullscreen(request.toggleOn())))
    window.setCentralWidget(view)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
