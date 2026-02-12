from owl.utils import widget_config
from qtpy import QtWidgets, QtCore
from owl.enums import Color


class Background(QtWidgets.QWidget):
    def __init__(self, color=Color.BACKGROUND):
        super().__init__()
        color = "rgb(10, 10, 10)" if color is Color.WINDOW else "rgb(23, 23, 23)"
        self._main_layout = QtWidgets.QVBoxLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setLayout(self._main_layout)
        self.setStyleSheet(f"""
Background
{{
    background: {color};
    border: 1px solid #1e293b;
    border-radius: 10px;
}}
""")

    def addWidget(self, widget):
        self._main_layout.addWidget(widget)
