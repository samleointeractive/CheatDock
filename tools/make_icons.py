"""Render assets/icon.svg into the PNG and ICO files the app and the .exe use.

Usage:  python tools/make_icons.py      (needs PySide6 and Pillow)
"""

from pathlib import Path

from PIL import Image
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]
PNG_SIZES = [16, 24, 32, 48, 64, 128, 256, 512]


def render(renderer: QSvgRenderer, size: int) -> Image.Image:
    img = QImage(size, size, QImage.Format.Format_RGBA8888)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(p, QRectF(0, 0, size, size))
    p.end()
    return Image.frombytes("RGBA", (size, size), bytes(img.constBits()))


def main() -> None:
    QGuiApplication([])
    renderer = QSvgRenderer(str(ASSETS / "icon.svg"))
    for size in PNG_SIZES:
        render(renderer, size).save(ASSETS / f"icon-{size}.png")
    # Each ICO size is rendered separately so small sizes stay crisp.
    frames = [render(renderer, s) for s in ICO_SIZES]
    frames[-1].save(ASSETS / "icon.ico", format="ICO", sizes=[(s, s) for s in ICO_SIZES],
                    append_images=frames[:-1])
    print("icons written to", ASSETS)


if __name__ == "__main__":
    main()
