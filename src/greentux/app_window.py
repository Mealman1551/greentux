from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtCore import QCoreApplication
from .webview import create_webview
from .config import TRAY_ICON_PATH


class GreenTuxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 700)
        self.setWindowTitle("GreenTux")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon(TRAY_ICON_PATH))
        self.webview = create_webview()
        self.setCentralWidget(self.webview)

        # Ctrl+Q om echt af te sluiten
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(QCoreApplication.instance().quit)

    def closeEvent(self, event):
        self.hide()
        event.ignore()
