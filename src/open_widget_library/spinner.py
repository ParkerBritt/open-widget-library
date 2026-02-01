from qtpy import QtWidgets, QtCore

class Spinner(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
