from owl.utils import widget_config
from qtpy import QtWidgets, QtCore
from owl.enums import Color
from .widget import Widget


class Background(Widget):
    def __init__(self, color=Color.BACKGROUND, styled=True):
        super().__init__()

        if not styled:
            return

        color = "rgb(10, 10, 10)" if color is Color.WINDOW else "rgb(23, 23, 23)"
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setStyleSheet(f"""
Background
{{
    background: {color};
    border: 1px solid #1e293b;
    border-radius: 10px;
}}
""")
