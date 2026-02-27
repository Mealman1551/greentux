#!/bin/bash
# Meal Installer v1.0
set -e

INSTALL_DIR="/opt/greentux"
DESKTOP_FILE="/usr/share/applications/greentux.desktop"

echo "Installing GreenTux to $INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r . "$INSTALL_DIR"
sudo ln -sf "$INSTALL_DIR/greentux" /usr/local/bin/greentux

echo "Creating start menu entry..."
sudo bash -c "cat > $DESKTOP_FILE" << EOF
[Desktop Entry]
Name=GreenTux
Comment=GreenTux is an open source WhatsApp client
Exec=/usr/local/bin/greentux
Icon=$INSTALL_DIR/assets/greentux_icon.png
Terminal=false
Type=Application
Categories=Utility;
EOF

echo "GreenTux is installed!"

if [ -f "README.txt" ]; then
   echo ""
   echo "===== README ====="
   cat README.txt
   echo "=================="
else
   echo "README.txt not found."
fi

echo ""
read -n 1 -s -r -p "Press any key to close..."
echo ""
