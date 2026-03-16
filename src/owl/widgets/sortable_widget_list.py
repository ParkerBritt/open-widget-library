from qtpy import QtWidgets, QtCore
import owl
import math

class SortableWidgetList(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setContentsMargins(0,0,0,0)

        self._backgrounds = list()

        self._selected_widget = None

        self._start_pos = QtCore.QPoint()
        self._widget_start_pos = QtCore.QPoint()
        self._last_pos = QtCore.QPoint()
        self._animations = {}
        self._original_positions = {}
        self._displaced = set()

    def mousePressEvent(self, event):
        selected_candidate = self.childAt(event.pos())
        selected_widget = None
        print("child before:", selected_candidate)
        while selected_candidate and selected_candidate != self:
            selected_candidate = selected_candidate.parent()
            
            property = selected_candidate.property("__owl_draggable__")
            print("property:", property)
            if property:
                selected_widget = selected_candidate

        print("child before after:", selected_candidate)

        if not selected_widget:
            return

        self._selected_widget = selected_widget

        self._selected_widget.raise_()

        self._start_pos = event.pos()
        self._widget_start_pos = self._selected_widget.pos()
        self._displaced = set()
        self._original_positions = {}
        for i in range(self._main_layout.count()):
            w = self._main_layout.itemAt(i).widget()
            self._original_positions[w] = w.pos()

    def mouseMoveEvent(self, event):
        last_pos = self._last_pos
        cur_pos = event.pos()
        self._last_pos = event.pos()

        if not self._selected_widget:
            return
        delta = event.pos() - self._start_pos
        new_pos = self._widget_start_pos + delta
        self._selected_widget.move(0, new_pos.y())

        selected_index = self._main_layout.indexOf(self._selected_widget)
        dragged_center_y = self._selected_widget.pos().y() + self._selected_widget.height() / 2

        for i in range(self._main_layout.count()):
            if i == selected_index:
                continue
            widget = self._main_layout.itemAt(i).widget()
            orig_pos = self._original_positions[widget]
            orig_center_y = orig_pos.y() + widget.height() / 2

            # Should this widget be displaced?
            should_displace = (
                (i > selected_index and dragged_center_y > orig_center_y) or
                (i < selected_index and dragged_center_y < orig_center_y)
            )

            if should_displace and widget not in self._displaced:
                self._displaced.add(widget)
                direction = -1 if i > selected_index else 1
                offset = self._selected_widget.height() + self._main_layout.spacing()
                end_pos = orig_pos + QtCore.QPoint(0, offset * direction)
                self._animate_widget(widget, end_pos)

            elif not should_displace and widget in self._displaced:
                self._displaced.discard(widget)
                self._animate_widget(widget, orig_pos)



    def _animate_widget(self, widget, end_pos):
        if widget in self._animations:
            self._animations[widget].stop()

        animation = QtCore.QPropertyAnimation(widget, b"pos", self)
        animation.setDuration(300)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        animation.setStartValue(widget.pos())
        animation.setEndValue(end_pos)
        animation.finished.connect(lambda w=widget: self._animations.pop(w, None))
        self._animations[widget] = animation
        animation.start()

    def mouseReleaseEvent(self, event):
        if not self._selected_widget:
            return
        # self._selected_widget.move(self._widget_start_pos)
        self._selected_widget = None
        self._main_layout.update()

    def add_widget(self, widget):
        container = owl.Background(color=owl.Color.WINDOW)
        container.setProperty("__owl_draggable__", True)
        container.add_widget(widget)
        self._main_layout.addWidget(container)

        self._backgrounds.append(widget)
        return self

