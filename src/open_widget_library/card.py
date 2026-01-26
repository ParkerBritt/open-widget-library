from . import widget_config
from qtpy import QtWidgets, QtCore

class Card(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.setStyleSheet(
"""
Card
{
    background: rgb(23, 23, 23);
    border: 1px solid rgba(255,255,255, 0.1);
    border-radius: 10px;
}
"""

        )
