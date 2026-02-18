from PySide6.QtWidgets import QStackedLayout
from owl.utils import widget_config
from qtpy import QtWidgets, QtCore
from owl.enums import Color


class StackedPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._main_layout = QtWidgets.QVBoxLayout()
        self._stacked_layout = QStackedLayout()
        self.setLayout(self._main_layout)
        #         self.setAttribute(QtCore.Qt.WA_StyledBackground)
        #         self.setStyleSheet(f"""
        # CodeBlock
        # {{
        #     background: {color};
        #     color: white;
        #     border: 1px solid #1e293b;
        #     border-radius: 10px;
        # }}
        # """)

        self._main_layout.addLayout(self._stacked_layout)
