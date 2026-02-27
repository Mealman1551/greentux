import os
import sys

APP_NAME = "GreenTux"


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        # gecompileerde versie — relatief aan executable
        base_path = os.path.dirname(sys.argv[0])
    else:
        # development — relatief aan project root
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    return os.path.join(base_path, relative_path)


PROFILE_DIR = os.path.expanduser("~/.greentux/profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

TRAY_ICON_PATH = resource_path("assets/greentux_icon.png")
