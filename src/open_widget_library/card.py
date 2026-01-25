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
    background: #171717;
    border: 2px solid #1e293b;
    border-radius: 10px;
}
"""

        )
