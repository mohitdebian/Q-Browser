import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.setWindowTitle("Simple Web Browser")
        self.setGeometry(0, 0, 800, 600)

        # Set up web view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        # Set up navigation bar
        navigation_bar = QToolBar("Navigation")
        self.addToolBar(navigation_bar)

        back_button = QAction(QIcon("icons/back.png"), "Back", self)
        back_button.triggered.connect(self.browser.back)
        navigation_bar.addAction(back_button)

        forward_button = QAction(QIcon("icons/forward.png"), "Forward", self)
        forward_button.triggered.connect(self.browser.forward)
        navigation_bar.addAction(forward_button)

        reload_button = QAction(QIcon("icons/reload.png"), "Reload", self)
        reload_button.triggered.connect(self.browser.reload)
        navigation_bar.addAction(reload_button)

        home_button = QAction(QIcon("icons/home.png"), "Home", self)
        home_button.triggered.connect(self.navigate_home)
        navigation_bar.addAction(home_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addWidget(self.url_bar)

        # Add Bootstrap CSS to the web view
        bootstrap_url = QUrl.fromLocalFile("path/to/bootstrap.min.css")
        css_injector = CssInjector(self.browser.page())
        css_injector.load(bootstrap_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

class CssInjector(QObject):
    def __init__(self, web_engine_page):
        super().__init__(web_engine_page)
        self._page = web_engine_page

    def load(self, url):
        self._url = url
        self._page.loadFinished.connect(self._on_load_finished)
        self._page.load(QUrl("about:blank"))

    def _on_load_finished(self, ok):
        if ok:
            with open(self._url.toLocalFile(), "r") as f:
                css = f.read()
                self._page.runJavaScript(
                    """
                    (function() {
                        var style = document.createElement('style');
                        style.innerHTML = `%s`;
                        document.head.appendChild(style);
                    })();
                    """ % css
                )
        else:
            print("Failed to load CSS")

app = QApplication(sys.argv)
browser = Browser()
browser.show()
sys.exit(app.exec_())
