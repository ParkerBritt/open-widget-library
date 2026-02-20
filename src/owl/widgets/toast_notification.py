from qtpy import QtWidgets, QtCore, QtGui


class ToastNotification(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
        text: str,
        margin: int = 1,
        background_color="#282828",
    ):
        super().__init__(parent)

        self._parent = parent
        self._text = text
        self._margin = margin
        self._duration_ms = 2000
        self._background_color = background_color

        self._init_layout()
        self._init_geometry()
        self._init_animation()
        self._init_timer()

        self._parent.installEventFilter(self)

    def notify(self):
        self.show()
        self.raise_()
        self._slide_in_animation.start()

    def set_duration(self, duration_ms):
        self._duration_ms = duration_ms

    def eventFilter(self, obj, event):
        if obj is self._parent and event.type() == QtCore.QEvent.Resize:
            self._reposition()
        return super().eventFilter(obj, event)

    def _reposition(self):
        if not self.isVisible():
            return

        self._init_geometry()

        self._slide_in_animation.setStartValue(self._start_pos)
        self._slide_in_animation.setEndValue(self._end_pos)
        self._slide_out_animation.setStartValue(self._end_pos)
        self._slide_out_animation.setEndValue(self._start_pos)

    def _init_layout(self):
        self._label = QtWidgets.QLabel(self._text)
        self._label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._label)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            f"""
ToastNotification {{
    background: {self._background_color};
    border-radius: 8px;
    border: 1px solid #3d3d3d;
}}"""
        )

    def _init_timer(self):
        show_timer = QtCore.QTimer(self)
        show_timer.setSingleShot(True)
        show_timer.timeout.connect(self._slide_out_animation.start)
        show_timer.start(self._duration_ms)

    def _on_finished(self):
        self.hide()

    def _init_animation(self):
        self._slide_in_animation = QtCore.QPropertyAnimation(self, b"pos")
        self._slide_in_animation.setDuration(300)
        self._slide_in_animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self._slide_in_animation.setStartValue(self._start_pos)
        self._slide_in_animation.setEndValue(self._end_pos)

        self._slide_out_animation = QtCore.QPropertyAnimation(self, b"pos")
        self._slide_out_animation.setDuration(300)
        self._slide_out_animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self._slide_out_animation.setStartValue(self._end_pos)
        self._slide_out_animation.setEndValue(self._start_pos)
        self._slide_out_animation.finished.connect(self._on_finished)

    def _init_geometry(self):
        # TODO: allow setting alignment as argument
        parent_rect = self._parent.rect()
        print("screen rect:", parent_rect)

        # Scale proportional to window
        # width = parent_rect.width() * 0.2
        # height = parent_rect.height() * 0.15

        width = self._label.sizeHint().width() + 40
        height = self._label.sizeHint().height() + 40

        x_margin = self._margin * parent_rect.width() * 0.01
        y_margin = self._margin * parent_rect.height() * 0.01

        # Bottom left
        # x = parent_rect.x() + parent_rect.width() - width - x_margin
        # y = parent_rect.y() + parent_rect.height() - height - y_margin

        # Top Middle
        x = parent_rect.x() + (parent_rect.width() - width) / 2
        y = parent_rect.y() + y_margin
        start_y = parent_rect.y() - height

        self.setGeometry(x, y, width, height)

        self._start_pos = QtCore.QPoint(x, start_y)
        self._end_pos = QtCore.QPoint(x, y)

