from . import widget_config
from qtpy import QtWidgets, QtCore

class Tabs(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._main_layout = QtWidgets.QVBoxLayout(self)

        self._button_layout = QtWidgets.QHBoxLayout()
        self._main_layout.addLayout(self._button_layout)

        self._button_group = QtWidgets.QButtonGroup()
        self._button_group.setExclusive(True)

        self._underline = QtWidgets.QWidget()
        self._underline.setFixedWidth(200)
        self._underline.setFixedHeight(50)
        self._underline.setStyleSheet("QWidget { background: red; }")

        self._main_layout.addWidget(self._underline)

        self.anim = QtCore.QPropertyAnimation(self._underline, b"pos")
        self.anim.setDuration(600)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def addTab(self, name: str):
        new_button = QtWidgets.QPushButton(name)
        # new_button.setStyleSheet("""
        # QPushButton
        # {
        #     background: transparent;
        #     border: none;
        # }
        # """)
        new_button.setCheckable(True)
        new_button.clicked.connect(lambda: self.onButtonPressed(new_button))
        self._button_group.addButton(new_button)
        self._button_layout.addWidget(new_button)

    def onButtonPressed(self, button):
        if self.anim.state() == QtCore.QAbstractAnimation.Running:
            self.anim.stop()

        self.anim.setStartValue(self._underline.pos())
        self.anim.setEndValue(button.pos())

        self.anim.start()
