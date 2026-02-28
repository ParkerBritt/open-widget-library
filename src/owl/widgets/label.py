from qtpy import QtWidgets, QtCore


class Label(QtWidgets.QLabel):
    _HEADING_STYLES = {
        0: {"scale": 1.0, "font-weight": "normal"},
        1: {"scale": 2.0, "font-weight": "700"},
        2: {"scale": 1.5, "font-weight": "600"},
        3: {"scale": 1.17, "font-weight": "600"},
        4: {"scale": 1.0, "font-weight": "500"},
    }

    def __init__(self, text: str = "", parent: QtWidgets.QWidget = None):
        super().__init__(text, parent)
        self._heading = 0
        self._base_font_size = self.font().pointSize()
        self._apply_style()

    def set_heading(self, level: int = 0):
        """Set heading level (1-4). Use 0 for normal label."""
        self._heading = max(0, min(level, 4))
        self._apply_style()
        return self

    def heading(self) -> int:
        return self._heading

    def _apply_style(self):
        style = self._HEADING_STYLES.get(self._heading, self._HEADING_STYLES[0])
        font_size = int(self._base_font_size * style["scale"])
        font_weight = style["font-weight"]
        self.setStyleSheet(f"""
Label {{
    color: rgba(255, 255, 255, 0.87);
    font-size: {font_size}pt;
    font-weight: {font_weight};
}}
""")
