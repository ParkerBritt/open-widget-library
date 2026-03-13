from __future__ import annotations
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
        self._speed = 0.05
        self._border_radius = 10

        self.setStyleSheet("border-radius: 20px;")

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)  # ~60 fps

    def set_border_radius(radius: int) -> DotMatrixBackgroundEffect:
        self._border_radius
        self._update_mask
        return self

    def get_border_radius() -> int:
        return self._border_radius

    def set_speed(speed: float):
        self._speed = speed

    def _tick(self):
        self._time += self._speed
        self.update()

    def _update_mask(self):
        self._clip_path = QtGui.QPainterPath()
        rect = QtCore.QRectF(self.rect())
        # TODO: use actual border width
        rect.adjust(1,1,-1,-1)
        self._clip_path.addRoundedRect(rect, self._border_radius, self._border_radius,)

    def _apply_mask(self, painter: QtGui.QPainter):
        painter.setClipPath(self._clip_path)

    def resizeEvent(self, event):
        if self._border_radius:
            self._update_mask()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        self._apply_mask(painter)

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
