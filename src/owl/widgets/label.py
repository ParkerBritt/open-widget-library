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
        self._font_multiplier = 1.0
        self._base_font_size = self.font().pointSize()
        self._font_weight = "normal"
        self._apply_style()

    def set_heading(self, level: int = 0):
        """Set heading level (1-4). Use 0 for normal label."""
        self._heading = max(0, min(level, 4))
        style = self._HEADING_STYLES[self._heading]
        self._font_multiplier = style["scale"]
        self._font_weight = style["font-weight"]
        self._apply_style()
        return self

    def set_bold(self, bold: bool = True):
        """Set font weight to bold (700) or normal."""
        self._font_weight = "700" if bold else "normal"
        self._apply_style()
        return self

    def set_font_scale(self, scale: float):
        """Set font size as a multiplier of the base font size."""
        self._font_multiplier = scale
        self._apply_style()
        return self

    def set_word_wrap(self, wrap: bool):
        self.setWordWrap(wrap)
        return self

    def set_size_policy(self, horizontal, vertical):
        self.setSizePolicy(horizontal, vertical)
        return self

    def set_text_block(self, block: bool = True):
        if block:
            self.set_word_wrap(True)
            self.set_size_policy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        else:
            self.set_word_wrap(False)
            self.set_size_policy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        return self

    def heading(self) -> int:
        return self._heading

    def _apply_style(self):
        font_size = int(self._base_font_size * self._font_multiplier)
        self.setStyleSheet(f"""
Label {{
    color: rgb(220, 220, 220);
    font-size: {font_size}pt;
    font-weight: {self._font_weight};
}}
""")
