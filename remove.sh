#!/bin/bash
# GreenTux Uninstaller
# Gebruik: ./remove.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

INSTALL_DIR="/opt/greentux"
SYMLINK="/usr/local/bin/greentux"
DESKTOP_FILE="/usr/share/applications/greentux.desktop"

echo -e "${GREEN}=== GreenTux Uninstaller ===${NC}"
echo ""

if [ -L "$SYMLINK" ]; then
    echo -e "${YELLOW}Removing symlink: $SYMLINK${NC}"
    sudo rm "$SYMLINK"
else
    echo "No symlink found at $SYMLINK"
fi

if [ -f "$DESKTOP_FILE" ]; then
    echo -e "${YELLOW}Removing start menu entry: $DESKTOP_FILE${NC}"
    sudo rm "$DESKTOP_FILE"
else
    echo "No .desktop file found at $DESKTOP_FILE"
fi

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Removing installation directory: $INSTALL_DIR${NC}"
    sudo rm -rf "$INSTALL_DIR"
else
    echo "No installation directory found at $INSTALL_DIR"
fi

echo ""
read -r -p "Remove session data (~/.greentux)? [y/N] " RESP
if [[ "$RESP" =~ ^[yYjJ]$ ]]; then
    if [ -d "$HOME/.greentux" ]; then
        rm -rf "$HOME/.greentux"
        echo -e "${YELLOW}~/.greentux removed.${NC}"
    else
        echo "No session data found at ~/.greentux"
    fi
fi

echo ""
echo -e "${GREEN}GreenTux has been removed.${NC}"
