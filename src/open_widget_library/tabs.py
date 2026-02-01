from . import widget_config
from .widget_config import widget_config
from qtpy import QtWidgets, QtCore

class Tabs(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._main_layout = QtWidgets.QVBoxLayout(self)

        self._button_layout = QtWidgets.QHBoxLayout()
        self._main_layout.addLayout(self._button_layout)

        self._button_group = QtWidgets.QButtonGroup()
        self._button_group.setExclusive(True)
        self._button_height = 30;
        self._button_padding = (0,0,0,0);

        self._underline = QtWidgets.QWidget(self)
        self._underline.setStyleSheet("QWidget { background: white; border-radius: 10px; }")

        self.underline_geometry_anim = QtCore.QPropertyAnimation(self._underline, b"geometry")
        self.underline_geometry_anim.setDuration(300)
        self.underline_geometry_anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._place_underline()

    def addTab(self, name: str):
        new_button = QtWidgets.QPushButton(name)
        new_button.setIcon(widget_config.get_icon("zap"))
        new_button.setFixedHeight(self._button_height)
        new_button.setStyleSheet("""
        QPushButton
        {
            background: transparent;
            border: none;
            color: white;
            border-radius: 10px;
        }
        QPushButton::checked
        {
            color: black;
        }
        QPushButton::hover
        {
            background-color: rgb(100,100,100);
        }
        QPushButton::hover::checked
        {
            background-color: transparent;
        }
        """)
        new_button.setCheckable(True)
        new_button.clicked.connect(lambda: self.onButtonPressed(new_button))
        new_button.stackUnder(self._underline)
        self._button_group.addButton(new_button)
        self._button_layout.addWidget(new_button)

        if len(self._button_group.buttons()) == 1:
            new_button.setChecked(True)
            QtCore.QTimer.singleShot(0, self._place_underline)

    def _underline_position_for(self, button):
        return QtCore.QRect(button.x(), button.y()+button.height(), button.width(), button.height())

    def _bubble_position_for(self, button):
        return QtCore.QRect(button.x()-self._button_padding[0], button.y()-self._button_padding[1], button.width()+self._button_padding[2], button.height()+self._button_padding[3]+self._button_padding[1])

    def _place_underline(self):
        button = self._button_group.checkedButton()
        self._underline.setGeometry(self._bubble_position_for(button))

    def onButtonPressed(self, button):
        if self.underline_geometry_anim.state() == QtCore.QAbstractAnimation.Running:
            self.underline_geometry_anim.stop()

        self.underline_geometry_anim.setStartValue(self._underline.geometry())
        self.underline_geometry_anim.setEndValue(self._bubble_position_for(button))

        self.underline_geometry_anim.start()
