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
_webview_ref = None  # globale referentie naar webview voor blob video overlay

DOWNLOAD_DIR = os.path.expanduser("~/.greentux/viddl")


def set_tray(tray):
    global _tray_ref
    _tray_ref = tray


def get_accept_language():
    """Bouw een Accept-Language header op basis van de systeemtaal.
    Bijvoorbeeld: 'nl,nl-NL;q=0.9,en;q=0.8'
    """
    locale = QLocale.system()
    short = locale.bcp47Name()  # bijv. 'nl-NL'
    lang_only = short.split("-")[0]  # bijv. 'nl'

    if lang_only == short.lower():
        return f"{lang_only},en;q=0.8"
    else:
        return f"{lang_only},{short};q=0.9,en;q=0.8"


class _PopupPage(QWebEnginePage):
    """
    Tijdelijke pagina die popup-navigatie opvangt (nieuwe tab/venster).
    - blob: URL  → inline video overlay in de app zelf
    - gewone URL → openen in standaard browser
    """

    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.urlChanged.connect(self._on_url_changed)

    def _on_url_changed(self, url: QUrl):
        url_str = url.toString()
        if not url_str or url_str == "about:blank":
            return
        if url_str.startswith("blob:"):
            if _webview_ref is not None:
                _webview_ref.page().runJavaScript(
                    f"""
                    (function() {{
                        var existing = document.getElementById('_greentux_video_overlay');
                        if (existing) existing.remove();
                        var overlay = document.createElement('div');
                        overlay.id = '_greentux_video_overlay';
                        overlay.style = 'position:fixed;top:0;left:0;width:100%;height:100%;'
                                      + 'background:rgba(0,0,0,0.92);z-index:99999;'
                                      + 'display:flex;align-items:center;justify-content:center;';
                        var video = document.createElement('video');
                        video.src = '{url_str}';
                        video.controls = true;
                        video.autoplay = true;
                        video.style = 'max-width:90%;max-height:90%;border-radius:8px;';
                        var close = document.createElement('button');
                        close.innerText = '✕';
                        close.style = 'position:absolute;top:16px;right:24px;font-size:24px;'
                                    + 'background:none;border:none;color:white;cursor:pointer;';
                        close.onclick = function() {{ overlay.remove(); }};
                        overlay.appendChild(video);
                        overlay.appendChild(close);
                        overlay.onclick = function(e) {{ if(e.target===overlay) overlay.remove(); }};
                        document.body.appendChild(overlay);
                    }})();
                    """
                )
        else:
            QDesktopServices.openUrl(url)
        self.deleteLater()


class GreenTuxPage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self._blank_page = None
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok):
        if ok:
            # Override Notification API zodat WhatsApp denkt dat het werkt
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

    def createWindow(self, window_type):
        """
        WhatsApp Web opent video's en bijlagen soms in een nieuw venster/tab.
        We vangen dit op en handelen de URL intern af.
        """
        return _PopupPage(self.profile(), self.parent())

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
    """
    Alle downloads (video, afbeelding, sticker, audio, document) worden
    opgeslagen in ~/.greentux/viddl
    """
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    suggested = download.suggestedFileName()
    download.setDownloadDirectory(DOWNLOAD_DIR)
    download.setDownloadFileName(suggested)
    download.accept()
    print(f"[GreenTux] Download gestart: {DOWNLOAD_DIR}/{suggested}")


def create_webview():
    global _webview_ref

    webview = QWebEngineView()
    _webview_ref = webview

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
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False
    )
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False
    )

    webview.load(QUrl("https://web.whatsapp.com"))
    return webview
