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
        self._foo = False
        self._animations = {}

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
            
        self._start_pos = event.pos()
        self._widget_start_pos = self._selected_widget.pos()

    def mouseMoveEvent(self, event):
        last_pos = self._last_pos
        cur_pos = event.pos()
        self._last_pos = event.pos()

        if not self._selected_widget:
            return
        delta = event.pos() - self._start_pos
        new_pos = self._widget_start_pos + delta
        self._selected_widget.move(0, new_pos.y())

        delta_y = int(math.copysign(1, (cur_pos-last_pos).y()))
        print("delta y:", delta_y)
        if delta_y == 0:
            print("early return", delta_y)
            return

        # if self._foo:
        #     return
        start_index = self._main_layout.indexOf(self._selected_widget)+delta_y
        end_index = self._main_layout.count() if delta_y > 0 else -1
        print("start", start_index)
        print("end", end_index)
        min_y = min(last_pos.y(), cur_pos.y())
        max_y = max(last_pos.y(), cur_pos.y())
        for i in range(start_index, end_index, delta_y):
            widget = self._main_layout.itemAt(i).widget()
            widget_center = widget.pos().y() + widget.height() / 2
            print(i, min_y, widget_center ,max_y)
            if not (min_y <= widget_center <= max_y):
                continue
            print("HERE!!!!!!!!!!!!!!!")
            start_pos = widget.pos()
            end_pos = start_pos-QtCore.QPoint(0, widget.height())*delta_y
            print("start pos:", start_pos)
            print("end pos:", end_pos)

            if widget in self._animations:
                self._animations[widget].stop()

            animation = QtCore.QPropertyAnimation(widget, b"pos", self)
            animation.setDuration(300)
            animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
            animation.setStartValue(start_pos)
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

