from qtpy import QtWidgets, QtCore
import owl


class SortableWidgetList(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._selected_widget = None
        self._start_pos = QtCore.QPoint()
        self._widget_start_pos = QtCore.QPoint()
        self._animations = {}
        self._original_positions = {}
        self._displaced = set()

    def mousePressEvent(self, event):
        candidate = self.childAt(event.pos())
        selected = None
        while candidate and candidate != self:
            candidate = candidate.parent()
            if candidate.property("__owl_draggable__"):
                selected = candidate

        if not selected:
            return

        self._selected_widget = selected
        selected.raise_()
        self._start_pos = event.pos()
        self._widget_start_pos = selected.pos()
        self._displaced = set()
        self._original_positions = {
            self._main_layout.itemAt(i).widget(): self._main_layout.itemAt(i).widget().pos()
            for i in range(self._main_layout.count())
        }

    def mouseMoveEvent(self, event):
        if not self._selected_widget:
            return

        delta = event.pos() - self._start_pos
        self._selected_widget.move(0, (self._widget_start_pos + delta).y())

        selected_index = self._main_layout.indexOf(self._selected_widget)
        dragged_center = self._selected_widget.pos().y() + self._selected_widget.height() / 2

        for i in range(self._main_layout.count()):
            if i == selected_index:
                continue
            widget = self._main_layout.itemAt(i).widget()
            orig_pos = self._original_positions[widget]
            orig_center = orig_pos.y() + widget.height() / 2

            should_displace = (
                (i > selected_index and dragged_center > orig_center) or
                (i < selected_index and dragged_center < orig_center)
            )
            is_displaced = widget in self._displaced

            if should_displace == is_displaced:
                continue

            if should_displace:
                self._displaced.add(widget)
                direction = -1 if i > selected_index else 1
                offset = self._selected_widget.height() + self._main_layout.spacing()
                self._animate_widget(widget, orig_pos + QtCore.QPoint(0, offset * direction))
            else:
                self._displaced.discard(widget)
                self._animate_widget(widget, orig_pos)

    def _animate_widget(self, widget, end_pos):
        if widget in self._animations:
            self._animations[widget].stop()
        anim = QtCore.QPropertyAnimation(widget, b"pos", self)
        anim.setDuration(300)
        anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        anim.setStartValue(widget.pos())
        anim.setEndValue(end_pos)
        anim.finished.connect(lambda w=widget: self._animations.pop(w, None))
        self._animations[widget] = anim
        anim.start()

    def mouseReleaseEvent(self, event):
        if not self._selected_widget:
            return
        self._selected_widget = None
        self._main_layout.update()

    def add_widget(self, widget):
        container = owl.Background(color=owl.Color.WINDOW)
        container.setProperty("__owl_draggable__", True)
        container.add_widget(widget)
        self._main_layout.addWidget(container)
        return self
