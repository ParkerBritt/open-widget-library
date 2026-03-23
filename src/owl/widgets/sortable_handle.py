from qtpy import QtWidgets, QtCore
import owl


class SortableHandle(QtWidgets.QWidget):
    def __init__(self, title=None):
        super().__init__()
        self._title = title

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(owl.Label(self._title or "").set_bold())
        self._main_layout.addWidget(owl.Icon("grip-vertical"))
        self.setProperty("__owl_handle__", True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setObjectName("test")
        self.setCursor(QtCore.Qt.OpenHandCursor)
        self.setStyleSheet("""
#test
{
    border-bottom: 1px solid #2F2F2F;
}

                           """)
