from owl.utils import widget_config
from qtpy import QtWidgets, QtCore
from owl.enums import Color


class Widget(QtWidgets.QWidget):
    # Directions
    Direction = QtWidgets.QBoxLayout.Direction
    LeftToRight = Direction.LeftToRight
    RightToLeft = Direction.RightToLeft
    TopToBottom = Direction.TopToBottom
    BottomToTop = Direction.BottomToTop

    def __init__(self, direction: Direction=LeftToRight , color=Color.BACKGROUND):
        super().__init__()
        self._main_layout = QtWidgets.QBoxLayout(direction)
        self.setLayout(self._main_layout)

    def set_margins(self, margin: int):
        self._main_layout.setContentsMargins(margin,margin,margin,margin)

    def add_widget(self, widget):
        self._main_layout.addWidget(widget)

    def addWidget(self, widget):
        self.add_widget(widget)

    def add_widgets(self, *widgets):
        for widget in widgets:
            self.add_widget(widget)

    def add_layout(self, layout):
        self._main_layout.addLayout(layout)
