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

GreenTux wraps WhatsApp Web in a polished native Linux desktop experience. Instead of keeping a browser tab open, you get a dedicated app with system tray integration, persistent sessions, and full desktop notification support -- all powered by an embedded Chromium engine that stays in sync with WhatsApp's own web interface automatically.

## Features

- **Persistent sessions** -- Scan the QR code once; your session is saved across restarts
- **System tray integration** -- Minimize to tray, get notifications, stay connected in the background
- **Desktop notifications** -- WhatsApp notifications are forwarded natively to your desktop
- **Microphone & camera support** -- Permissions are granted automatically for voice and video calls
- **KDE Plasma 6 / Wayland compatible** -- Runs on Wayland via XCB compatibility layer
- **Dark theme** -- A custom dark mode stylesheet
- **Always up to date** -- Loads `web.whatsapp.com` directly; no reverse engineering, no maintenance

## How It Works

GreenTux embeds a Chromium browser via **PyQt6-WebEngine** and loads `web.whatsapp.com`. This means it is always compatible with the latest WhatsApp Web features without any additional updates on your end.

- A **named `QWebEngineProfile`** stores cookies and `localStorage` in `~/.greentux/profile`, preserving your login between sessions
- The **user agent** is set to a standard Chrome/Linux string so WhatsApp Web accepts the browser without issues
- A custom **`QWebEnginePage`** subclass intercepts `featurePermissionRequested` to automatically grant microphone, camera, and notification permissions
- **Desktop notifications** are captured via Qt's `setNotificationPresenter` and forwarded to the tray icon's `showMessage`

## Building and Installing

> Build on **Ubuntu 24.04**. This ensures the widest compatibility with other distros due to the glibc version.

**1. Install dependencies**

```bash
chmod +x scripts/install-build-deps.sh
./scripts/install-build-deps.sh
```

This installs gcc, patchelf, Nuitka, and PyQt6 with WebEngine via pip. It will also remove the system version of PyQt6 if present, since that causes Qt version mismatches when running on other distros.

**2. Compile**

```bash
chmod +x scripts/compile.sh
./scripts/compile.sh
```

**3. Install**

```bash
chmod +x install.sh
./install.sh
```

GreenTux will be installed to `/opt/greentux` and will appear in your start menu. The `greentux` command will also be available in your PATH.

**To uninstall:**

```bash
chmod +x remove.sh
./remove.sh
```

This removes the app and optionally clears your session data in `~/.greentux`.

---

## Usage

Launch GreenTux from the start menu or by running `greentux` in a terminal. Scan the QR code with your phone the first time. After that, your session is remembered automatically.

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **`Ctrl + Q`** | Quit the application |

> [!WARNING]
> Closing the window does **not** quit the app -- it minimizes GreenTux to the system tray. To fully exit, use **Ctrl + Q**.

### Tray Icon

| Action | Result |
|--------|--------|
| **Left-click** | Toggle window visibility |

## Platform Notes

### KDE Plasma 6 / Wayland

GreenTux forces `QT_QPA_PLATFORM=xcb` on startup to ensure tray icon signals work correctly under Wayland. This is handled automatically -- no manual configuration needed.

## Configuration

Session data and profile storage are kept in:

```
~/.greentux/profile/
```

To reset your session (for example to log in with a different account), delete this directory and restart the app.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

GPLv3

---

Made with 💚 by Mealman1551

---

###### &copy; 2026 Mealman1551
