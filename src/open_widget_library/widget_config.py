from pathlib import Path
from qtpy import QtWidgets, QtCore, QtGui, QtSvg

border_radius = 10


class WidgetConfig:
    def __init__(self):
        self._icons = {}
        self._PACKAGE_ROOT = Path(__file__).resolve().parent
        self._ICONS_DIR = self._PACKAGE_ROOT / "resources" / "icons" / "lucide"

    @property
    def stylesheet(self):
        style_string = """
    QWidget
    {
        border
    }
    """
        return style_string

    def set_svg_color(self, svg: str, color: str) -> str:
        return svg.replace("<svg", f'<svg style="color:{color};"', 1)

    def get_icon_pixmap(self, icon_name, color: str | None = None, scale=16):
        dir = str(self._ICONS_DIR / f"{icon_name}.svg")

        svg = open(dir, encoding="utf-8").read()

        if color:
            svg = self.set_svg_color(svg, color)

        renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg.encode("utf-8")))

        pixmap = QtGui.QPixmap(scale, scale)
        pixmap.fill(QtGui.QColor(0, 0, 0, 0))
        p = QtGui.QPainter(pixmap)
        renderer.render(p)
        p.end()

        return pixmap

    def get_icon_svg(self, icon_name, color: str | None = None, scale=16):
        dir = str(self._ICONS_DIR / f"{icon_name}.svg")

        svg = open(dir, encoding="utf-8").read()

        if color:
            svg = self.set_svg_color(svg, color)

        return QtCore.QByteArray(svg)

    def get_icon(self, icon_name, color: str | None = None):
        icon = self._icons.get(icon_name)
        dir = str(self._ICONS_DIR / f"{icon_name}.svg")

        svg = open(dir, encoding="utf-8").read()

        if color:
            svg = self.set_svg_color(svg, color)

        renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg.encode("utf-8")))

        if not icon:
            icon = QtGui.QIcon()

            for pixmap_scale in (16, 20, 24, 32, 64):
                pm = QtGui.QPixmap(pixmap_scale, pixmap_scale)
                pm.fill(QtGui.QColor(0, 0, 0, 0))
                p = QtGui.QPainter(pm)
                renderer.render(p)
                p.end()
                icon.addPixmap(pm)

        return icon


widget_config = WidgetConfig()
