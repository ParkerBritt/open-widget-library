from . import widget_config
from qtpy import QtWidgets, QtCore

class Background(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
"""
Background
{
    background: rgb(10, 10, 10);
    border: 1px solid #1e293b;
}
"""

        )
