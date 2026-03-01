import os

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QSystemTrayIcon
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineSettings,
    QWebEnginePage,
    QWebEngineNotification,
    QWebEngineDownloadRequest,
)
from PyQt6.QtCore import QUrl, QLocale
from PyQt6.QtGui import QDesktopServices
from .config import PROFILE_DIR

_tray_ref = None  # globale referentie naar tray voor notificaties


def set_tray(tray):
    global _tray_ref
    _tray_ref = tray


def get_accept_language():
    locale = QLocale.system()
    short = locale.bcp47Name()
    lang_only = short.split("-")[0]

    if lang_only == short.lower():
        return f"{lang_only},en;q=0.8"
    else:
        return f"{lang_only},{short};q=0.9,en;q=0.8"


class GreenTuxPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self._blank_page = None
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok):
        if ok:
            # override Notification API zodat WhatsApp denkt dat het werkt
            self.runJavaScript(
                """
                const _OrigNotification = window.Notification;
                window.Notification = function(title, options) {
                    return new _OrigNotification(title, options);
                };
                Object.defineProperty(window.Notification, 'permission', {
                    get: () => 'granted'
                });
                window.Notification.requestPermission = () => Promise.resolve('granted');
            """
            )

    def featurePermissionRequested(self, url, feature):
        allowed = [
            QWebEnginePage.Feature.Notifications,
            QWebEnginePage.Feature.MediaAudioCapture,
            QWebEnginePage.Feature.MediaVideoCapture,
            QWebEnginePage.Feature.MediaAudioVideoCapture,
            QWebEnginePage.Feature.DesktopAudioVideoCapture,
        ]
        if feature in allowed:
            self.setFeaturePermission(
                url, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
        else:
            self.setFeaturePermission(
                url, feature, QWebEnginePage.PermissionPolicy.PermissionDeniedByUser
            )


def handle_notification(notification: QWebEngineNotification):
    notification.show()
    if _tray_ref is not None:
        _tray_ref.showMessage(
            notification.title(),
            notification.message(),
            QSystemTrayIcon.MessageIcon.Information,
            5000,  # 5 seconden zichtbaar
        )


def handle_download(download: QWebEngineDownloadRequest):
    downloads_dir = os.path.expanduser("~/.greentux/viddl")
    os.makedirs(downloads_dir, exist_ok=True)
    suggested = download.suggestedFileName()
    download.setDownloadDirectory(downloads_dir)
    download.setDownloadFileName(suggested)
    download.accept()
    print(f"Downloaden: {downloads_dir}/{suggested}")


def create_webview():
    webview = QWebEngineView()

    profile = QWebEngineProfile("greentux", webview)
    profile.setPersistentStoragePath(PROFILE_DIR)
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
    )
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    profile.setCachePath(PROFILE_DIR + "/cache")
    profile.setNotificationPresenter(handle_notification)
    profile.downloadRequested.connect(handle_download)

    profile.setHttpUserAgent(
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )

    # Stel de taal in op basis van de systeemtaal zodat WhatsApp Web
    # automatisch de juiste taal laadt
    profile.setHttpAcceptLanguage(get_accept_language())

    page = GreenTuxPage(profile, webview)
    webview.setPage(page)
    webview.setZoomFactor(1.0)

    settings = webview.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)

    webview.load(QUrl("https://web.whatsapp.com"))
    return webview
