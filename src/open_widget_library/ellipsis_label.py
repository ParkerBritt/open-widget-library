from qtpy import QtWidgets, QtCore, QtGui

class EllipsisLabel(QtWidgets.QLabel):
    def __init__(self, text="", parent=None, elide_mode=QtCore.Qt.ElideMiddle):
        super().__init__(parent)
        self._full_text = text
        self._elide_mode = elide_mode

        super().setText(text)

        self.setMinimumWidth(0)
        self.setWordWrap(False)

        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)

    def setText(self, text):
        self._full_text = text
        super().setText(text)
        self.update()

    def text(self):
        return self._full_text

    # Custom drawing elided version of text
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        # Draw QLabel background/border/etc
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)

        # Respect QLabel margins
        rect = self.contentsRect()

        # Create Elided text
        metrics = QtGui.QFontMetrics(self.font())

        lines = self._full_text.splitlines()
        elided_lines = [
            metrics.elidedText(line, self._elide_mode, rect.width()) for line in lines
        ]
        elided_text = "\n".join(elided_lines)

        # Respect alignment like a normal QLabel
        flags = self.alignment()
        painter.drawText(rect, flags, elided_text)
