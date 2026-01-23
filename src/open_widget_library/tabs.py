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

        self._underline = QtWidgets.QWidget(self)
        # self._underline.setFixedWidth(200)
        self._underline.setFixedHeight(2)
        self._underline.setStyleSheet("QWidget { background: white; border-radius: 1px; }")

        self.underline_geometry_anim = QtCore.QPropertyAnimation(self._underline, b"geometry")
        self.underline_geometry_anim.setDuration(600)
        self.underline_geometry_anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._place_underline()

    def addTab(self, name: str):
        new_button = QtWidgets.QPushButton(name)
        new_button.setStyleSheet("""
        QPushButton
        {
            background: transparent;
            border: none;
            color: white;
        }
        """)
        new_button.setCheckable(True)
        new_button.clicked.connect(lambda: self.onButtonPressed(new_button))
        self._button_group.addButton(new_button)
        self._button_layout.addWidget(new_button)

        if len(self._button_group.buttons()) == 1:
            new_button.setChecked(True)
            # self._place_underline(new_button)
            QtCore.QTimer.singleShot(0, self._place_underline)

    def _place_underline(self):
        button = self._button_group.checkedButton()

        end = QtCore.QRect(button.x(), button.y()+button.height(), button.width(), button.height())
        self._underline.setGeometry(end)

    def onButtonPressed(self, button):
        if self.underline_geometry_anim.state() == QtCore.QAbstractAnimation.Running:
            self.underline_geometry_anim.stop()

        self.underline_geometry_anim.setStartValue(self._underline.geometry())
        print("cur geo:", self._underline.geometry())
        end = QtCore.QRect(button.x(), button.y()+button.height(), button.width(), button.height())
        self.underline_geometry_anim.setEndValue(end)
        print("new geo:", button.geometry())

        self.underline_geometry_anim.start()
