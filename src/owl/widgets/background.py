from owl.utils import widget_config
from qtpy import QtWidgets, QtCore, QtGui
from owl.enums import Color
from .widget import Widget
from .container import Container
import random
from enum import IntEnum, auto


class Background(Widget):
    def __init__(self, color=Color.BACKGROUND, styled=True):
        # super(Widget, self).__init__()
        super().__init__()
        # self._main_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)

        if not styled:
            return

        self._color = "#0a0a0a" if color is Color.WINDOW else "#171717"
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet(f"""
Background
{{
    background: {self._color};
    border: 1px solid #2F2F2F;
    border-radius: 10px;
}}
""")

        self._background_effect = None

    def set_effect(self, background_effect: QtWidgets.QGraphicsScene = None):
        self._background_effect = background_effect
        self._background_effect.setParent(self)
        self._background_effect.show()

    # def _init_graphics_view(self):
    #     self._graphics_view = BackgroundGraphicsView(self)
    #
    #     self._graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    #     self._graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    #     self._graphics_view.setFrameStyle(QtWidgets.QFrame.NoFrame)
    #
    #     self._graphics_view.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    #     self._graphics_view.setSizePolicy(
    #         QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
    #     )
    #     self._graphics_view.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

    def resizeEvent(self, event: QtGui.QResizeEvent):
        if self._background_effect:
            self._background_effect.setGeometry(self.rect())
        super().resizeEvent(event)


class BackgroundGraphicsView(QtWidgets.QGraphicsView):
    def paintEvent(self, event):
        self.radius = 10
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        rect = self.rect()
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)

        painter.setClipPath(path)
        painter.fillPath(path, self.palette().window())

        super().paintEvent(event)
