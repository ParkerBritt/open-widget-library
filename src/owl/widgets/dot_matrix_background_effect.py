import math

from qtpy import QtCore, QtGui, QtWidgets


class DotMatrixBackgroundEffect(QtWidgets.QWidget):
    def __init__(
        self,
        dot_spacing: int = 24,
        dot_radius: float = 1.5,
        color: QtGui.QColor = QtGui.QColor(255, 255, 255, 80),
    ):
        super().__init__()
        self._dot_spacing = dot_spacing
        self._dot_radius = dot_radius
        self._color = color
        self._time = 0.0

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)  # ~60 fps

    def _tick(self):
        self._time += 0.05
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        w = self.width()
        h = self.height()
        spacing = self._dot_spacing
        base_r = self._dot_radius
        cx, cy = w / 2, h / 2

        cols = w // spacing + 2
        rows = h // spacing + 2

        c = self._color
        for row in range(rows):
            for col in range(cols):
                x = col * spacing
                y = row * spacing

                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                wave = math.sin(dist * 0.02 - self._time) * 0.5 + 0.5

                r = base_r * (0.4 + wave * 0.6)
                alpha = int(c.alpha() * (0.3 + wave * 0.7))

                painter.setBrush(QtGui.QColor(c.red(), c.green(), c.blue(), alpha))
                painter.drawEllipse(QtCore.QPointF(x, y), r, r)

        painter.end()
