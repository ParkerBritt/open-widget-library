from enum import IntEnum, auto
from typing import Optional
from qtpy import QtWidgets, QtCore, QtGui, QtSvgWidgets

from owl.utils import widget_config


class Icon(QtWidgets.QWidget):
    class RenderMode(IntEnum):
        SVG = auto()
        PIXMAP = auto()

    class Size(IntEnum):
        # TODO: Implement
        DEFAULT = auto()  # get size from config
        FILL = auto()  # fill container

    def __init__(
        self,
        icon_name: Optional[str] = None,
        file_path: Optional[str] = None,
        file_path_selected: Optional[str] = None,
        size=Size.DEFAULT,
    ):
        super().__init__()

        # TODO: implement default size
        self._size = 14
        self.setFixedSize(self._size, self._size)

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        if icon_name:
            self._mode = self.RenderMode.SVG

            print("setting normal svg for", icon_name)
            self._normal_svg = widget_config.get_icon_svg(icon_name, "white")
            self._selected_svg = widget_config.get_icon_svg(icon_name, "black")

            self._icon_svg_widget = SVGWidget()
            # self._icon_svg_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            print("here size no timer:", self._icon_svg_widget.size())
            QtCore.QTimer.singleShot(
                1000, lambda: print("here size:", self._icon_svg_widget.size())
            )
            self._icon_svg_widget.load(self._normal_svg)
            self._icon_svg_widget.renderer().setAspectRatioMode(QtCore.Qt.KeepAspectRatio)

            self._main_layout.addWidget(self._icon_svg_widget)
        elif file_path:
            self._mode = self.RenderMode.PIXMAP

            # self._normal_pixmap = widget_config.get_icon_pixmap(icon, "white")
            # self._selected_pixmap = widget_config.get_icon_pixmap(icon, "black")
            self._normal_pixmap = QtGui.QPixmap(file_path)
            self._selected_pixmap = QtGui.QPixmap(file_path_selected or file_path)

            self._icon_pixmap_widget = PixmapLabel(pixmap=self._normal_pixmap)

            self._main_layout.addWidget(self._icon_pixmap_widget)
        else:
            raise ValueError(
                "Icon must have either a supported icon name or path to pixmap/svg file."
            )

        self._selected = False

    def set_selected(self, selected: bool = True):
        self._selected = selected

        if self._mode is self.RenderMode.SVG:
            svg = self._selected_svg if self._selected else self._normal_svg
            self._icon_svg_widget.load(svg)
            self._icon_svg_widget.renderer().setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        elif self._mode is self.RenderMode.PIXMAP:
            pixmap = self._selected_pixmap if self._selected else self._normal_pixmap
            self._icon_pixmap_widget.setSourcePixmap(pixmap)


class PixmapLabel(QtWidgets.QLabel):
    def __init__(self, parent=None, pixmap=None):
        super().__init__(parent)
        self._pixmap_src = None
        self.setAlignment(QtCore.Qt.AlignCenter)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        if pixmap:
            self.setSourcePixmap(pixmap)

    def setSourcePixmap(self, pixmap: QtGui.QPixmap):
        self._pixmap_src = pixmap
        self._update_scaled()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_scaled()

    def _update_scaled(self):
        if not self._pixmap_src or self.width() <= 0 or self.height() <= 0:
            return
        size = self.size()
        max_size = max(size.width(), size.height())
        scaled = self._pixmap_src.scaled(
            QtCore.QSize(max_size, max_size),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        print("size", self.size())
        super().setPixmap(scaled)


class SVGWidget(QtSvgWidgets.QSvgWidget):
    def resizeEvent(self, e):
        super().resizeEvent(e)
        side = self.height()
        if self.minimumWidth() != side or self.maximumWidth() != side:
            self.setMinimumWidth(side)
            self.setMaximumWidth(side)
