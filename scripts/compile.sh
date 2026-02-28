#!/bin/bash
set -e
cd ..

PYTHONPATH=src python3 -m nuitka \
  --standalone \
  --enable-plugin=pyqt6 \
  --include-qt-plugins=sensible,webengine \
  --include-data-dir=themes=themes \
  --include-data-dir=assets=assets \
  --include-package=greentux \
  --output-dir=build \
  greentux.py

# WebEngine heeft deze resources nodig naast de binary
QTWE=$(python3 -c "import PyQt6; import os; print(os.path.dirname(PyQt6.__file__))")/Qt6

DIST=build/greentux.dist

# Kopieer ontbrekende WebEngine bestanden
mkdir -p $DIST/PyQt6/Qt6/translations
mkdir -p $DIST/PyQt6/Qt6/resources  
mkdir -p $DIST/PyQt6/Qt6/libexec

cp -rn $QTWE/translations/qtwebengine_locales $DIST/PyQt6/Qt6/translations/ 2>/dev/null || true
cp -n $QTWE/resources/qtwebengine_resources.pak $DIST/PyQt6/Qt6/resources/ 2>/dev/null || true
cp -n $QTWE/resources/qtwebengine_devtools_resources.pak $DIST/PyQt6/Qt6/resources/ 2>/dev/null || true
cp -n $QTWE/resources/qtwebengine_resources_100p.pak $DIST/PyQt6/Qt6/resources/ 2>/dev/null || true
cp -n $QTWE/resources/icudtl.dat $DIST/PyQt6/Qt6/resources/ 2>/dev/null || true
cp -n $QTWE/resources/v8_context_snapshot.bin $DIST/PyQt6/Qt6/resources/ 2>/dev/null || true
cp -n $QTWE/libexec/QtWebEngineProcess $DIST/PyQt6/Qt6/libexec/ 2>/dev/null || true

echo "Build klaar in $DIST"