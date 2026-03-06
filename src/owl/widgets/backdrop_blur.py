from qtpy import QtWidgets, QtCore, QtGui


class BackdropBlur(QtWidgets.QWidget):
    def __init__(self, background: QtWidgets.QWidget):
        super().__init__(background)
        self._background = background
        self._cached: QtGui.QPixmap | None = None

    def showEvent(self, event):
        super().showEvent(event)
        QtCore.QTimer.singleShot(0, self._capture)

    def _capture(self):
        src = QtGui.QPixmap(self._background.size())
        self._background.render(
            src, QtCore.QPoint(), QtGui.QRegion(), QtWidgets.QWidget.RenderFlag.DrawWindowBackground
        )

        effect = getattr(self._background, "_background_effect", None)
        if effect is not None:
            painter = QtGui.QPainter(src)
            effect.render(
                painter, effect.pos(), QtGui.QRegion(), QtWidgets.QWidget.RenderFlag.DrawChildren
            )
            painter.end()

        radius = 50
        pos = self.mapTo(self._background, QtCore.QPoint(0, 0))

        # Expand capture region by the blur radius on all sides so the blur
        # kernel has real pixels to sample at the edges instead of bleeding black.
        # Clamp to the background bounds so we don't go out of range.
        expanded = QtCore.QRect(
            pos.x() - radius, pos.y() - radius,
            self.width() + radius * 2, self.height() + radius * 2,
        ).intersected(self._background.rect())

        blurred = _blur(src.copy(expanded), radius=radius)

        # Crop back to our actual size, accounting for how much we could expand.
        inner_x = pos.x() - expanded.x()
        inner_y = pos.y() - expanded.y()
        self._cached = blurred.copy(inner_x, inner_y, self.width(), self.height())
        self.update()

    def paintEvent(self, event):
        if self._cached is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self._cached)
        painter.end()


def _blur(pixmap: QtGui.QPixmap, radius: int) -> QtGui.QPixmap:
    scene = QtWidgets.QGraphicsScene()
    item = scene.addPixmap(pixmap)
    effect = QtWidgets.QGraphicsBlurEffect()
    effect.setBlurRadius(radius)
    item.setGraphicsEffect(effect)
    result = QtGui.QPixmap(pixmap.size())
    result.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(result)
    scene.render(painter)
    painter.end()
    return result
