from owl.utils import widget_config
from qtpy import QtWidgets, QtCore
from owl.enums import Color


class CodeBlock(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        color = "rgb(23, 23, 23)"
        self._main_layout = QtWidgets.QVBoxLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setLayout(self._main_layout)
        self.setStyleSheet(f"""
CodeBlock
{{
    background: {color};
    color: white;
    border: 1px solid #1e293b;
    border-radius: 10px;
}}
""")

        self._main_layout.addWidget(QtWidgets.QLabel("Hello world foo bar"))
