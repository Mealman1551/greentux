import sys
import os
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

os.environ["QT_QPA_PLATFORM"] = "xcb"  # moet voor Qt imports!

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from .app_window import GreenTuxWindow
from .tray import create_tray
from .webview import set_tray
from .config import TRAY_ICON_PATH

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(TRAY_ICON_PATH))
window = GreenTuxWindow()
tray = create_tray(app, window)
set_tray(tray)

with open("themes/dark.qss") as f:
    app.setStyleSheet(f.read())

window.show()
sys.exit(app.exec())
