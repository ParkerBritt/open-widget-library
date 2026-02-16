from qtpy import QtWidgets, QtCore, QtGui
from .icon import Icon


class TabButton(QtWidgets.QPushButton):
    def __init__(self, name: str, icon: Icon = None):
        super().__init__()

        self._name = name
        self._icon = icon
        self._left_padding = 5

        self._init_layout()

    def _init_layout(self):
        self._label = QtWidgets.QLabel(self._name)

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._main_layout.addSpacing(self._left_padding)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setAlignment(QtCore.Qt.AlignLeft)
        if self._icon:
            self._main_layout.addWidget(self._icon)
        self._main_layout.addWidget(self._label)

        self.toggled.connect(self._on_toggled)

        self.setStyleSheet("""
        QPushButton
        {
            background: transparent;
            border: none;
            color: white;
            border-radius: 10px;
        }
        QPushButton QLabel
        {
            color: white;
        }
        QPushButton QLabel[selected="true"]
        {
            color: black;
        }
        """)

    def _on_toggled(self, state):
        if self._icon:
            self._icon.set_selected(state)

        self._label.setProperty("selected", state)
        self._label.style().unpolish(self._label)
        self._label.style().polish(self._label)
        self._label.update()


class Tabs(QtWidgets.QWidget):
    def __init__(
        self, parent=None, orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
    ):
        super().__init__(parent)
        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._orientation = orientation
        if orientation is QtCore.Qt.Orientation.Horizontal:
            self._button_layout = QtWidgets.QHBoxLayout()
        else:
            self._button_layout = QtWidgets.QVBoxLayout()
            self._button_layout.setAlignment(QtCore.Qt.AlignTop)

        self._main_layout.addLayout(self._button_layout)

        self._button_group = QtWidgets.QButtonGroup()
        self._button_group.setExclusive(True)
        self._button_height = 30
        self._button_padding = (0, 0, 0, 0)

        self._underline = QtWidgets.QWidget(self)
        self._underline.setStyleSheet("QWidget { background: white; border-radius: 10px; }")

        self.underline_geometry_anim = QtCore.QPropertyAnimation(self._underline, b"geometry")
        self.underline_geometry_anim.setDuration(300)
        self.underline_geometry_anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

        self._icons: list = list()
        self._icons_selected: list = list()

        self._last_selected_button = None

        self.index_by_button_id = dict()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._place_underline()

    def addTab(self, name: str, icon: Icon = None):
        new_button = TabButton(name, icon)

        # new_button = QtWidgets.QPushButton()
        #
        # layout = QtWidgets.QHBoxLayout(new_button)
        # label = QtWidgets.QLabel(name)
        # label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        # label.setObjectName("tabLabel")
        # icon_label = QtWidgets.QLabel()
        # layout.addWidget(icon_label)
        # layout.addWidget(label)
        #
        #
        # self._icons.append(icon)
        # self._icons_selected.append(selected_icon)
        #
        # if(icon):
        #     icon_label.setIcon(icon)
        #
        new_button.setFixedHeight(self._button_height)
        new_button.setCheckable(True)
        new_button.clicked.connect(lambda: self.onButtonPressed(new_button))
        new_button.stackUnder(self._underline)

        button_index = len(self._button_group.buttons())

        self._button_group.addButton(new_button)
        self._button_layout.addWidget(new_button)

        button_id = self._button_group.id(new_button)
        self.index_by_button_id[button_id] = button_index

        # new_button.setStyleSheet("""
        # QPushButton
        # {
        #     background: transparent;
        #     border: none;
        #     color: white;
        #     border-radius: 10px;
        # }
        # QPushButton QLabel
        # {
        #     color: white;
        # }
        # QPushButton QLabel[selected="true"]
        # {
        #     color: black;
        # }
        # """)
        #
        # def on_toggled(on):
        #     label.setProperty("selected", on)
        #     label.style().unpolish(label)
        #     label.style().polish(label)
        #     label.update()
        #
        # new_button.toggled.connect(on_toggled)

        if button_index == 0:
            new_button.setChecked(True)
            QtCore.QTimer.singleShot(0, self._place_underline)

    def _underline_position_for(self, button):
        return QtCore.QRect(
            button.x(), button.y() + button.height(), button.width(), button.height()
        )

    def _bubble_position_for(self, button):
        return QtCore.QRect(
            button.x() - self._button_padding[0],
            button.y() - self._button_padding[1],
            button.width() + self._button_padding[2],
            button.height() + self._button_padding[3] + self._button_padding[1],
        )

    def _place_underline(self):
        button = self._button_group.checkedButton()
        self._underline.setGeometry(self._bubble_position_for(button))

    def onButtonPressed(self, button):
        if self.underline_geometry_anim.state() == QtCore.QAbstractAnimation.Running:
            self.underline_geometry_anim.stop()

        self.underline_geometry_anim.setStartValue(self._underline.geometry())
        self.underline_geometry_anim.setEndValue(self._bubble_position_for(button))

        self.underline_geometry_anim.start()

        button_id = self._button_group.id(button)
        index = self.index_by_button_id.get(button_id)

        # unselected_icon = self._icons[index]
        # if(self._last_selected_button and unselected_icon):
        #     self._last_selected_button.setIcon(unselected_icon)
        #
        # selected_icon = self._icons_selected[index]
        # if(selected_icon):
        #     button.setIcon(selected_icon)

        self._last_selected_button = button
