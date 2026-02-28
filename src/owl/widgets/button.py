from __future__ import annotations
from qtpy import QtWidgets, QtCore


class Button(QtWidgets.QPushButton):
    def __init__(self, text: str = "", parent: QtWidgets.QWidget = None):
        super().__init__(text, parent)

        self.setStyleSheet(f"""
Button
{{
    background: #151515;
    border: 1px solid #2F2F2F;
    border-radius: 7px;
    color: rgba(255, 255, 255, 0.87);
    padding: 4px 16px;
}}

Button:hover
{{
    background: #1C1C1C
}}
""")

    def fill_width(self, fill: bool) -> Button:
        size_policy = self.sizePolicy()
        print("size policy", size_policy)
        horizontal_policy = QtWidgets.QSizePolicy.Minimum if fill else QtWidgets.QSizePolicy.Maximum
        size_policy.setHorizontalPolicy(horizontal_policy)
        self.setSizePolicy(size_policy)
        return self
