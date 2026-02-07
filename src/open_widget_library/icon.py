from enum import IntEnum
from typing import Optional
from qtpy import QtWidgets, QtCore, QtGui, QtSvgWidgets

from . import widget_config


class Icon(QtWidgets.QWidget):
    class RenderMode(IntEnum):
        SVG = 0
        PIXMAP = 1

    def __init__(
        self, icon: Optional[str] = None, file_path: Optional[str] = None, file_path_selected: Optional[str] = None
    ):
        super().__init__()

        if not (icon or file_path):
            raise ValueError("Icon must have either a supported icon name or path to pixmap/svg file.")

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        if icon:
            self._mode = self.RenderMode.SVG

            print("setting normal svg for", icon)
            self._normal_svg = widget_config.get_icon_svg(icon, "white")
            self._selected_svg = widget_config.get_icon_svg(icon, "black")

            self._icon_svg_widget = QtSvgWidgets.QSvgWidget()
            self._icon_svg_widget.load(self._normal_svg)
            self._icon_svg_widget.renderer().setAspectRatioMode(QtCore.Qt.KeepAspectRatio)

            self._main_layout.addWidget(self._icon_svg_widget)
        elif file_path:
            self._mode = self.RenderMode.PIXMAP

            print("setting normal pixmap for", icon)
            # self._normal_pixmap = widget_config.get_icon_pixmap(icon, "white")
            # self._selected_pixmap = widget_config.get_icon_pixmap(icon, "black")
            self._normal_pixmap = QtGui.QPixmap(file_path)
            self._selected_pixmap = QtGui.QPixmap(file_path_selected or file_path)

            self._icon_pixmap_widget = QtWidgets.QLabel()
            self._icon_pixmap_widget.setPixmap(self._normal_pixmap)

            self._main_layout.addWidget(self._icon_pixmap_widget)

        self._selected = False

    def set_selected(self, selected: bool = True):
        self._selected = selected

        if self._mode is self.RenderMode.SVG:
            svg = self._selected_svg if self._selected else self._normal_svg
            self._icon_svg_widget.load(svg)
            self._icon_svg_widget.renderer().setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        elif self._mode is self.RenderMode.PIXMAP:
            pixmap = self._selected_pixmap if self._selected else self._normal_pixmap
            self._icon_pixmap_widget.setPixmap(pixmap)
