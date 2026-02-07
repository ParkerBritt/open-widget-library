from qtpy import QtWidgets, QtCore, QtGui

from . import widget_config


class Icon(QtWidgets.QWidget):
    def __init__(self, icon: str):
        super().__init__()

        self._normal_pixmap = widget_config.get_icon_pixmap(icon, "white")
        self._selected_pixmap = widget_config.get_icon_pixmap(icon, "black")

        self._icon_label = QtWidgets.QLabel()
        self._icon_label.setPixmap(self._normal_pixmap)

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._icon_label)

        self._selected = False

    def set_selected(self, selected: bool = True):
        self._selected = selected

        pixmap = self._selected_pixmap if self._selected else self._normal_pixmap
        self._icon_label.setPixmap(pixmap)
