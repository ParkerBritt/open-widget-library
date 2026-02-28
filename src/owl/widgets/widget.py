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

    def __init__(
        self, direction: QtWidgets.QBoxLayout.Direction = LeftToRight, color=Color.BACKGROUND
    ):
        super().__init__()
        self.set_main_layout(QtWidgets.QBoxLayout(direction))

    def set_layout_direction(self, direction: QtWidgets.QBoxLayout.Direction):
        self._main_layout.setDirection(direction)

    def set_main_layout(self, layout):
        self._main_layout = layout
        super().setLayout(self._main_layout)

    def setLayout(self, layout):
        self.set_main_layout(layout)

    def set_margins(self, margin: int):
        self._main_layout.setContentsMargins(margin, margin, margin, margin)

    def add_widget(self, widget):
        self._main_layout.addWidget(widget)

    def addWidget(self, widget):
        self.add_widget(widget)

    def add_widgets(self, *widgets):
        for widget in widgets:
            self.add_widget(widget)

    def add_layout(self, layout):
        self._main_layout.addLayout(layout)
