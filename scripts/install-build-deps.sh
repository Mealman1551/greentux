#!/bin/bash
# GreenTux - build dependency installer
# Installs everything needed to build GreenTux with Nuitka
# Supports: Debian/Ubuntu (apt), Fedora/RHEL (dnf), Arch (pacman), openSUSE (zypper)
# Usage: ./scripts/install-build-deps.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}=== GreenTux - Dependency Installer ===${NC}"
echo ""

# ──────────────────────────────────────────────
# Detect package manager
# ──────────────────────────────────────────────
if command -v apt &>/dev/null; then
    DISTRO="apt"
    DISTRO_NAME="Debian / Ubuntu / Linux Mint"
elif command -v dnf &>/dev/null; then
    DISTRO="dnf"
    DISTRO_NAME="Fedora / RHEL / CentOS"
elif command -v pacman &>/dev/null; then
    DISTRO="pacman"
    DISTRO_NAME="Arch Linux / Manjaro / EndeavourOS"
elif command -v zypper &>/dev/null; then
    DISTRO="zypper"
    DISTRO_NAME="openSUSE"
else
    echo -e "${RED}No supported package manager found.${NC}"
    echo "Please install manually: gcc, patchelf, ccache, python3, pip3, libxcb-cursor"
    exit 1
fi

echo -e "${BLUE}Distro: $DISTRO_NAME${NC}"
echo ""

# ──────────────────────────────────────────────
# Step 1: System packages
# ──────────────────────────────────────────────
echo -e "${YELLOW}[1/3] Installing system packages...${NC}"

case "$DISTRO" in
    apt)
        sudo apt update
        sudo apt install -y \
            python3 python3-pip python3-dev \
            gcc patchelf ccache \
            libxcb-cursor0
        ;;
    dnf)
        sudo dnf install -y \
            python3 python3-pip python3-devel \
            gcc patchelf ccache \
            xcb-util-cursor
        ;;
    pacman)
        sudo pacman -Sy --noconfirm \
            python python-pip \
            gcc patchelf ccache \
            xcb-util-cursor
        ;;
    zypper)
        sudo zypper install -y \
            python3 python3-pip python3-devel \
            gcc patchelf ccache \
            libxcb-cursor0
        ;;
esac

# ──────────────────────────────────────────────
# Step 2: Remove system PyQt6 if present
# System PyQt6 causes Qt version mismatches when
# running on other distros, so we always use pip.
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[2/3] Checking for system PyQt6...${NC}"

PYQT6_LOCATION=$(python3 -c "
import sys
for path in sys.path:
    import os
    candidate = os.path.join(path, 'PyQt6')
    if os.path.isdir(candidate):
        print(candidate)
        break
" 2>/dev/null || echo "")

if [ -z "$PYQT6_LOCATION" ]; then
    echo -e "${BLUE}PyQt6 not found, will be installed via pip.${NC}"
elif echo "$PYQT6_LOCATION" | grep -q "dist-packages"; then
    echo -e "${YELLOW}System PyQt6 found at $PYQT6_LOCATION, removing...${NC}"
    case "$DISTRO" in
        apt)
            sudo apt purge -y \
                python3-pyqt6 \
                python3-pyqt6.qtwebengine \
                python3-pyqt6.qtqml \
                python3-pyqt6.qtwebchannel 2>/dev/null || true
            sudo apt autoremove -y
            ;;
        dnf)
            sudo dnf remove -y python3-pyqt6 python3-qt6-webengine 2>/dev/null || true
            ;;
        pacman)
            sudo pacman -R --noconfirm python-pyqt6 2>/dev/null || true
            ;;
        zypper)
            sudo zypper remove -y python3-PyQt6 2>/dev/null || true
            ;;
    esac
    echo -e "${GREEN}System PyQt6 removed.${NC}"
else
    echo -e "${GREEN}pip version already active ($PYQT6_LOCATION), skipping removal.${NC}"
fi

# ──────────────────────────────────────────────
# Step 3: Install Python packages via pip
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[3/3] Installing Python packages via pip...${NC}"
echo -e "${BLUE}(This downloads ~250MB of Qt6 libraries)${NC}"
echo ""

pip3 install --break-system-packages \
    PyQt6 \
    PyQt6-Qt6 \
    PyQt6-WebEngine \
    PyQt6-WebEngine-Qt6 \
    nuitka \
    ordered-set

# ──────────────────────────────────────────────
# Verify
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"

FAILED=false

check() {
    local label="$1"
    local cmd="$2"
    if eval "$cmd" &>/dev/null; then
        echo -e "${GREEN}✓ $label${NC}"
    else
        echo -e "${RED}✗ $label${NC}"
        FAILED=true
    fi
}

check "Python3"           "python3 --version"
check "pip3"              "pip3 --version"
check "gcc"               "gcc --version"
check "patchelf"          "patchelf --version"
check "Nuitka"            "python3 -m nuitka --version"
check "PyQt6"             "python3 -c 'import PyQt6'"
check "PyQt6.QtWebEngine" "python3 -c 'import PyQt6.QtWebEngineWidgets'"
check "libxcb-cursor"     "ldconfig -p | grep -q libxcb-cursor"

# Check that the pip version is active, not system
FINAL_LOCATION=$(python3 -c "
import sys
for path in sys.path:
    import os
    candidate = os.path.join(path, 'PyQt6')
    if os.path.isdir(candidate):
        print(candidate)
        break
" 2>/dev/null || echo "")

if echo "$FINAL_LOCATION" | grep -q "dist-packages"; then
    echo -e "${RED}✗ PyQt6 is still the system version ($FINAL_LOCATION)${NC}"
    FAILED=true
else
    echo -e "${GREEN}✓ PyQt6 pip version active ($FINAL_LOCATION)${NC}"
fi

echo ""
if [ "$FAILED" = true ]; then
    echo -e "${RED}Some dependencies failed to install.${NC}"
    echo "This is not critical and will work fine in most cases, though you may occasionally encounter issues when compiling or running GreenTux."
    exit 1
else
    echo -e "${GREEN}=== All done! ===${NC}"
    echo ""
    echo "Next step:"
    echo "  ./scripts/compile.sh"
fi
