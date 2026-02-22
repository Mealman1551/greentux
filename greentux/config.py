import os

APP_NAME = "GreenTux"
PROFILE_DIR = os.path.expanduser("~/.greentux/profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

TRAY_ICON_PATH = os.path.join(os.path.dirname(__file__), "../assets/greentux_icon.png")
