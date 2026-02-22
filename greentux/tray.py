from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtCore import QCoreApplication
from .config import TRAY_ICON_PATH


def create_tray(app, window):
    icon = QIcon(TRAY_ICON_PATH)
    if icon.isNull():
        icon = app.style().standardIcon(app.style().StandardPixmap.SP_ComputerIcon)

    tray_icon = QSystemTrayIcon(icon, parent=app)

    tray_menu = QMenu()
    show_action = QAction("Open GreenTux")
    quit_action = QAction("Afsluiten")

    show_action.triggered.connect(lambda: _show_window(window))
    quit_action.triggered.connect(lambda: _quit(tray_icon))

    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)
    tray_icon.setContextMenu(tray_menu)

    def on_activated(reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if window.isVisible():
                window.hide()
            else:
                _show_window(window)

    tray_icon.activated.connect(on_activated)
    tray_icon.show()
    return tray_icon


def _show_window(window):
    window.show()
    window.raise_()
    window.activateWindow()


def _quit(tray_icon):
    tray_icon.hide()
    QCoreApplication.instance().quit()
