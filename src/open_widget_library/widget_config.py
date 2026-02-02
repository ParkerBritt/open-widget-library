from pathlib import Path
from qtpy import QtWidgets, QtCore, QtGui, QtSvg
border_radius = 10;

class WidgetConfig():
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
        return svg.replace(
            "<svg",
            f'<svg style="color:{color};"',
            1
        )

    def get_icon(self, icon_name):
        icon = self._icons.get(icon_name)
        dir = str(self._ICONS_DIR / f"{icon_name}.svg")

        svg = open(dir, encoding="utf-8").read()

        red_svg = self.set_svg_color(svg, "#e11d48")

        renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(red_svg.encode("utf-8")))

        if not icon:
            icon = QtGui.QIcon()

            for pixmap_scale in (16,20,24,32,64):
                pm = QtGui.QPixmap(pixmap_scale, pixmap_scale)
                pm.fill(QtGui.QColor(0,0,0,0))
                p = QtGui.QPainter(pm)
                renderer.render(p)
                p.end()
                icon.addPixmap(pm)


        return icon

widget_config = WidgetConfig()
