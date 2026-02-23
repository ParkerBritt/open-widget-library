from owl.utils import widget_config
from qtpy import QtWidgets, QtCore, QtGui
from owl.enums import Color
from .widget import Widget
from .container import Container
import random


class Background(Widget):
    def __init__(self, color=Color.BACKGROUND, styled=True):
        # super(Widget, self).__init__()
        super().__init__()
        # self._main_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)

        if not styled:
            return

        self._styled_background = color is Color.WINDOW
        self._color = "#0a0a0a" if color is Color.WINDOW else "#171717"
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet(f"""
Background
{{
    background: {self._color};
    border: 1px solid #1e293b;
    border-radius: 10px;
}}
""")

        if self._styled_background:
            self._init_graphics_view()

    def _make_blurred_sphere(
        self, diameter: int = 200, color: QtGui.QColor = QtGui.QColor("purple")
    ):
        radius = diameter // 2

        pixmap = QtGui.QPixmap(diameter, diameter)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)
        gradient = QtGui.QRadialGradient(radius, radius, diameter)
        gradient.setColorAt(0, QtGui.QColor(color.red(), color.green(), color.blue(), 100))
        # gradient.setColorAt(0.3, QtGui.QColor(color.red(), color.green(), color.blue(), 70))
        gradient.setColorAt(0.5, QtGui.QColor(color.red(), color.green(), color.blue(), 0))
        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(0, 0, diameter, diameter)

        return pixmap

    def _init_graphics_view(self):
        # TODO: replace stacked layout with custom implementaiton of stacked layout
        # self._stacked_layout = QtWidgets.QStackedLayout()
        # super(Widget, self).setLayout(self._stacked_layout)
        #
        self._graphics_scene = QtWidgets.QGraphicsScene()
        self._graphics_view = QtWidgets.QGraphicsView(self)

        self._graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._graphics_view.setFrameStyle(QtWidgets.QFrame.NoFrame)

        self._pixmap_one = self._graphics_scene.addPixmap(self._make_blurred_sphere(diameter=1200))
        self._pixmap_two = self._graphics_scene.addPixmap(self._make_blurred_sphere(diameter=1200))
        # self._graphics_scene.addEllipse(0, 0, 200, 200, brush=QtGui.QBrush("red"))

        self._graphics_view.setScene(self._graphics_scene)
        self._graphics_view.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._graphics_view.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._graphics_view.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

        content_container = Container()
        content_container.add_layout(self._main_layout)

        # self._stacked_layout.addWidget(content_container)
        # self._stacked_layout.addWidget(self._graphics_view)
        #
        # self._stacked_layout.setStackingMode(QtWidgets.QStackedLayout.StackAll)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        if not self._styled_background:
            return

        size = event.size()
        border_size = 1
        view_rect = QtCore.QRect(
            border_size, border_size, size.width() - border_size, size.height() - border_size
        )
        self._graphics_scene.setSceneRect(view_rect)
        self._graphics_view.setGeometry(view_rect)
        self._graphics_view.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._graphics_view.setStyleSheet("background: transparent;")

        # path = QtGui.QPainterPath()

        self._graphics_view.setGraphicsEffect(RoundedCornerGraphicsEffect(10, self))

        tl = self._graphics_view.mapToScene(QtCore.QPoint(0, 0))
        br = self._graphics_view.mapToScene(QtCore.QPoint(size.width() - 1, size.height() - 1))

        r1 = self._pixmap_one.boundingRect()
        r2 = self._pixmap_two.boundingRect()

        # Top-left
        self._pixmap_one.setPos(tl.x() - r2.width() / 2, tl.y() - r2.height() / 2)

        # Bottom-right (subtract pixmap size so it fits in the corner)
        self._pixmap_two.setPos(br.x() - r2.width() / 2, br.y() - r2.height() / 2)


class RoundedCornerGraphicsEffect(QtWidgets.QGraphicsEffect):
    def __init__(self, radius: int, parent: QtCore.QObject | None = None):
        super().__init__(parent)
        self._radius = radius

    def draw(self, painter: QtGui.QPainter) -> None:
        offset = QtCore.QPoint()
        src = self.sourcePixmap(QtCore.Qt.LogicalCoordinates, offset)
        if src.isNull():
            return

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, src.width(), src.height(), self._radius, self._radius)
        painter.setClipPath(path, QtCore.Qt.IntersectClip)
        painter.drawPixmap(offset, src)
