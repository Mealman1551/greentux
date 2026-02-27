<div align="center">
  <img src="assets/greentux_icon.png" alt="GreenTux Logo" width="120"/>

  # GreenTux

  **A native Linux desktop client for WhatsApp Web**

  ![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
  ![Qt6](https://img.shields.io/badge/Qt-6-green?logo=qt)
  ![Platform](https://img.shields.io/badge/Platform-Linux-orange?logo=linux)
  ![License](https://img.shields.io/badge/License-GPLv3-orange)

</div>

---

GreenTux wraps WhatsApp Web in a polished native Linux desktop experience. Instead of keeping a browser tab open, you get a dedicated app with system tray integration, persistent sessions, and full desktop notification support — all powered by an embedded Chromium engine that stays in sync with WhatsApp's own web interface automatically.

## Features

- **Persistent sessions** — Scan the QR code once; your session is saved across restarts
- **System tray integration** — Minimize to tray, get notifications, stay connected in the background
- **Desktop notifications** — WhatsApp notifications are forwarded natively to your desktop
- **Microphone & camera support** — Permissions are granted automatically for voice and video calls
- **KDE Plasma 6 / Wayland compatible** — Runs on Wayland via XCB compatibility layer
- **Dark theme** — A custom stylesheet with a green accent that matches the GreenTux identity
- **Always up to date** — Loads `web.whatsapp.com` directly; no reverse engineering, no maintenance

## How It Works

GreenTux embeds a Chromium browser via **PyQt6-WebEngine** and loads `web.whatsapp.com`. This means it is always compatible with the latest WhatsApp Web features without any additional updates on your end.

- A **named `QWebEngineProfile`** stores cookies and `localStorage` in `~/.greentux/profile`, preserving your login between sessions
- The **user agent** is set to a standard Chrome/Linux string so WhatsApp Web accepts the browser without issues
- A custom **`QWebEnginePage`** subclass intercepts `featurePermissionRequested` to automatically grant microphone, camera, and notification permissions
- **Desktop notifications** are captured via Qt's `setNotificationPresenter` and forwarded to the tray icon's `showMessage`

## Requirements

- Python 3.13
- PyQt6
- PyQt6-WebEngine

Install dependencies:

```bash
pip install PyQt6 PyQt6-WebEngine
```

Or:

```bash
sudo apt install python3-pyqt6
sudo apt install python3-pyqt6.qtwebengine
```

## Installation

```bash
git clone https://github.com/Mealman1551/greentux.git
cd greentux
pip install -r requirements.txt
python greentux.py
```

## Usage

Launch GreenTux and scan the QR code with your phone the first time. After that, your session is remembered automatically.

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **`Ctrl + Q`** | **Quit the application** |

> [!Warning]
> Closing the window does **not** quit the app  it minimizes GreenTux to the system tray. To fully exit, use **`Ctrl + Q`**.

### Tray Icon

| Action | Result |
|--------|--------|
| Left-click | Toggle window visibility |

## Platform Notes

### KDE Plasma 6 / Wayland

GreenTux forces `QT_QPA_PLATFORM=xcb` on startup to ensure tray icon signals work correctly under Wayland. This is handled automatically — no manual configuration needed.

## Project Structure

```
greentux/
├── greentux.py        # Main application entry point
├── greentux_icon.svg  # Application icon
├── style.qss          # Dark theme stylesheet
└── README.md
```

## Configuration

Session data and profile storage are kept in:

```
~/.greentux/profile/
```

To reset your session (e.g. to log in as a different account), simply delete this directory and restart the app.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

GPLv3

---

###### &copy; 2026 Mealman1551

---

Made with 💚 by Mealman1551