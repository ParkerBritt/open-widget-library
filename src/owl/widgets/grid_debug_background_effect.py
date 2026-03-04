import random
from qtpy import QtWidgets, QtGui, QtCore


class GridDebugBackgroundEffect(QtWidgets.QWidget):
    def __init__(self, cell_size: int = 64):
        super().__init__()
        self._cell_size = cell_size
        self._colors: dict[tuple, QtGui.QColor] = {}

    def _color_for(self, col: int, row: int) -> QtGui.QColor:
        key = (col, row)
        if key not in self._colors:
            self._colors[key] = QtGui.QColor(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        return self._colors[key]

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        s = self._cell_size
        cols = self.width() // s + 1
        rows = self.height() // s + 1
        for col in range(cols):
            for row in range(rows):
                painter.fillRect(col * s, row * s, s, s, self._color_for(col, row))
        painter.end()
