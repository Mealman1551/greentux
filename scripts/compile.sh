cd ~/git-projects/greentux

rm -rf build

PYTHONPATH=src python3 -m nuitka \
  --standalone \
  --enable-plugin=pyqt6 \
  --include-qt-plugins=sensible \
  --include-data-dir=themes=themes \
  --include-data-dir=assets=assets \
  --include-package=greentux \
  --output-dir=build \
  greentux.py