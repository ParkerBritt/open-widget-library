from qtpy import QtWidgets, QtCore
from .widget import Widget


class Container(Widget):
    def __init__(self):
        super().__init__()

        self.set_margins(0)
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
