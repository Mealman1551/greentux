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
from PyQt6.QtCore import QUrl
from .config import PROFILE_DIR, MEDIA_DIR

_tray_ref = None


def set_tray(tray):
    global _tray_ref
    _tray_ref = tray


class GreenTuxPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok):
        if ok:
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
            5000,
        )


def handle_download(download: QWebEngineDownloadRequest):
    """Auto-download media naar ~/.greentux/viddl, prompt voor de rest."""
    mime = download.mimeType() or ""
    suggested = download.suggestedFileName() or "download"

    # Media types die WhatsApp Web als download stuurt (video, gif, sticker, afbeelding)
    is_media = (
        mime.startswith("video/")
        or mime.startswith("image/")
        or mime.startswith("audio/")
        or suggested.lower().endswith(
            (".mp4", ".webm", ".gif", ".webp", ".jpg", ".jpeg", ".png", ".opus", ".ogg")
        )
    )

    if is_media:
        os.makedirs(MEDIA_DIR, exist_ok=True)
        download.setDownloadDirectory(MEDIA_DIR)
        download.setDownloadFileName(suggested)
        download.accept()
    else:
        # Binaire bestanden (PDF, docx, etc.) → prompt zoals voorheen
        from PyQt6.QtWidgets import QFileDialog

        default_path = os.path.join(os.path.expanduser("~"), "Downloads", suggested)
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        save_path, _ = QFileDialog.getSaveFileName(None, "Opslaan als", default_path)
        if save_path:
            download.setDownloadDirectory(os.path.dirname(save_path))
            download.setDownloadFileName(os.path.basename(save_path))
            download.accept()
        else:
            download.cancel()


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
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    page = GreenTuxPage(profile, webview)
    webview.setPage(page)
    webview.setZoomFactor(1.0)

    settings = webview.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False
    )
    settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)

    webview.load(QUrl("https://web.whatsapp.com"))
    return webview
