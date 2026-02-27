#!/bin/bash
# Meal Uninstaller v1.0
set -e

INSTALL_DIR="/opt/greentux"
SYMLINK="/usr/local/bin/greentux"
DESKTOP_FILE="/usr/share/applications/greentux.desktop"

echo "Removing GreenTux..."

if [ -L "$SYMLINK" ]; then
   echo "Removing symlink $SYMLINK"
   sudo rm "$SYMLINK"
else
   echo "No symlink found at $SYMLINK"
fi

if [ -f "$DESKTOP_FILE" ]; then
   echo "Removing start menu entry $DESKTOP_FILE"
   sudo rm "$DESKTOP_FILE"
else
   echo "No .desktop file found at $DESKTOP_FILE"
fi

if [ -d "$INSTALL_DIR" ]; then
   echo "Removing installation directory $INSTALL_DIR"
   sudo rm -rf "$INSTALL_DIR"
else
   echo "No installation directory found at $INSTALL_DIR"
fi

echo "GreenTux has been removed!"
