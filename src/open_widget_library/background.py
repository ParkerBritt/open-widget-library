from . import widget_config
from qtpy import QtWidgets, QtCore

class Background(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
"""
Background
{
    background: #020817;
    border: 1px solid #1e293b;
}
"""

        )
