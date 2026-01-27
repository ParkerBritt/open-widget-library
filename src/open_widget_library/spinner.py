from . import widget_config
from qtpy import QtWidgets, QtCore

class Spinner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
