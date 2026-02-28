#!/bin/bash
# GreenTux - Nuitka compiler
# Gebruik: ./scripts/compile.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

cd "$(dirname "$0")/.."

echo -e "${GREEN}=== GreenTux - Build ===${NC}"
echo ""

# Controleer Nuitka
if ! python3 -m nuitka --version &>/dev/null; then
    echo -e "${RED}Nuitka not found. Run first:${NC}"
    echo "  ./scripts/install-build-deps.sh"
    exit 1
fi

# Controleer pip PyQt6 (niet systeem versie)
PYQT6_PATH=$(python3 -c "import PyQt6; import os; print(os.path.dirname(PyQt6.__file__))" 2>/dev/null || echo "")
if echo "$PYQT6_PATH" | grep -q "dist-packages"; then
    echo -e "${RED}ERROR: System version of PyQt6 detected ($PYQT6_PATH)${NC}"
    echo "This causes Qt version mismatches on other distros."
    echo "Run ./scripts/install-build-deps.sh to fix this."
    exit 1
fi

echo -e "${YELLOW}PyQt6: $PYQT6_PATH${NC}"
echo -e "${YELLOW}Nuitka: $(python3 -m nuitka --version 2>&1 | head -1)${NC}"
echo ""

# Schoon oude build op
rm -rf build/greentux.dist build/greentux.build

# Compileer
PYTHONPATH=src python3 -m nuitka \
    --standalone \
    --enable-plugin=pyqt6 \
    --include-qt-plugins=sensible \
    --include-data-dir=themes=themes \
    --include-data-dir=assets=assets \
    --include-package=greentux \
    --output-dir=build \
    greentux.py

# Hernoem greentux.bin naar greentux
mv build/greentux.dist/greentux.bin build/greentux.dist/greentux

echo ""
echo -e "${GREEN}=== Build complete ===${NC}"
echo ""
echo "Binary: build/greentux.dist/greentux"
echo ""
echo "To install:"
echo "  ./install.sh"
