#!/bin/bash
# GreenTux Installer
# Gebruik: ./install.sh (vanuit de projectroot, na ./scripts/compile.sh)

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

INSTALL_DIR="/opt/greentux"
SYMLINK="/usr/local/bin/greentux"
DESKTOP_FILE="/usr/share/applications/greentux.desktop"
DIST="$(cd "$(dirname "$0")" && pwd)/build/greentux.dist"

echo -e "${GREEN}=== GreenTux Installer ===${NC}"
echo ""

# Controleer of de build aanwezig is
if [ ! -f "$DIST/greentux" ]; then
    echo -e "${RED}ERROR: build/greentux.dist/greentux not found.${NC}"
    echo "Build first with:"
    echo "  ./scripts/compile.sh"
    exit 1
fi

echo -e "${YELLOW}Installing to: $INSTALL_DIR${NC}"
echo ""

# Installeer de dist map
sudo rm -rf "$INSTALL_DIR"
sudo cp -r "$DIST" "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/greentux"

# Symlink zodat 'greentux' in PATH werkt
sudo ln -sf "$INSTALL_DIR/greentux" "$SYMLINK"

# Desktop entry voor start menu
echo -e "${YELLOW}Creating start menu entry...${NC}"
sudo bash -c "cat > $DESKTOP_FILE" << EOF
[Desktop Entry]
Name=GreenTux
Comment=GreenTux is an open source WhatsApp client for Linux
Exec=$SYMLINK
Icon=$INSTALL_DIR/assets/greentux_icon.png
Terminal=false
Type=Application
Categories=Network;InstantMessaging;
StartupNotify=true
EOF

echo ""
echo -e "${GREEN}=== GreenTux installed! ===${NC}"
echo ""
echo "Launch from the start menu or run:"
echo "  greentux"
echo ""
read -n 1 -s -r -p "Press any key to close..."
echo ""
