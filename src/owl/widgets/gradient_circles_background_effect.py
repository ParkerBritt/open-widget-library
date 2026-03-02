from qtpy import QtWidgets, QtCore, QtGui


class GradientCirclesBackgroundEffect(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._init_graphics_view()
        self._graphics_scene = QtWidgets.QGraphicsScene(self)
        self._pixmap_one = self._graphics_scene.addPixmap(self._make_blurred_sphere(diameter=1200))
        self._pixmap_two = self._graphics_scene.addPixmap(self._make_blurred_sphere(diameter=1200))

        self._graphics_view.setScene(self._graphics_scene)
        self._graphics_view.show()

    def _init_graphics_view(self):
        self._graphics_view = QtWidgets.QGraphicsView(self)

        self._graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._graphics_view.setFrameStyle(QtWidgets.QFrame.NoFrame)

        self._graphics_view.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self._graphics_view.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self._graphics_view.setBackgroundBrush(QtGui.QColor(0, 0, 0, 0))

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

    def resizeEvent(self, event: QtGui.QResizeEvent):
        size = event.size()
        print("resize event", size)
        border_size = 1
        view_rect = QtCore.QRect(
            border_size, border_size, size.width() - border_size, size.height() - border_size
        )
        self._graphics_scene.setSceneRect(view_rect)
        self._graphics_view.setGeometry(view_rect)
        self._graphics_view.setStyleSheet("background: transparent;")

        tl = self._graphics_view.mapToScene(QtCore.QPoint(0, 0))
        br = self._graphics_view.mapToScene(QtCore.QPoint(size.width() - 1, size.height() - 1))

        r1 = self._pixmap_one.boundingRect()
        r2 = self._pixmap_two.boundingRect()

        # Top-left
        self._pixmap_one.setPos(tl.x() - r2.width() / 2, tl.y() - r2.height() / 2)

        # Bottom-right (subtract pixmap size so it fits in the corner)
        self._pixmap_two.setPos(br.x() - r2.width() / 2, br.y() - r2.height() / 2)
