from qtpy import QtWidgets, QtCore, QtGui
from .icon import Icon


class Tabs(QtWidgets.QWidget):
    index_changed = QtCore.Signal(int)

    def __init__(
        self, parent=None, orientation: QtCore.Qt.Orientation = QtCore.Qt.Orientation.Horizontal
    ):
        super().__init__(parent)

        self._icons: list = list()
        self._icons_selected: list = list()
        self._last_selected_button = None
        self._index_by_button_id = dict()
        self._button_id_count = 0
        self._largest_button_width = 0
        self._orientation = orientation

        self._init_layout()


    def _init_layout(self):
        # TODO: convert to box layout same as widget
        if self._orientation is QtCore.Qt.Orientation.Horizontal:
            self._button_layout = QtWidgets.QHBoxLayout(self)
        else:
            self._button_layout = QtWidgets.QVBoxLayout(self)
            self._button_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self._button_group = QtWidgets.QButtonGroup()
        self._button_group.setExclusive(True)
        self._button_height = 30
        self._button_padding = (0, 0, 0, 0)
        self._button_group.idClicked.connect(self._on_id_clicked)

        self._underline = QtWidgets.QWidget(self)
        self._underline.setStyleSheet("QWidget { background: white; border-radius: 10px; }")

        self.underline_geometry_anim = QtCore.QPropertyAnimation(self._underline, b"geometry")
        self.underline_geometry_anim.setDuration(300)
        self.underline_geometry_anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)


    def _on_id_clicked(self, id):
        index = self._index_by_button_id[id]
        self.index_changed.emit(index)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._place_underline()

    def addTab(self, name: str, icon: Icon = None) -> int:
        new_button = TabButton(name, icon)

        button_width = new_button.sizeHint().width()
        if(self._largest_button_width < button_width):
            self._largest_button_width = button_width
            self.setMaximumWidth(self._largest_button_width*2)

        new_button.setFixedHeight(self._button_height)
        new_button.setCheckable(True)
        new_button.clicked.connect(lambda: self.onButtonPressed(new_button))
        new_button.stackUnder(self._underline)

        button_index = len(self._button_group.buttons())

        self._button_group.addButton(new_button)
        self._button_layout.addWidget(new_button)

        button_id = self._button_group.id(new_button)
        self._index_by_button_id[button_id] = button_index

        if button_index == 0:
            new_button.setChecked(True)
            QtCore.QTimer.singleShot(0, self._place_underline)

        return button_id

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

        self._last_selected_button = button


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
        self._spacing_widget = QtWidgets.QWidget()
        self._spacing_widget.setFixedWidth(self._left_padding)
        self._main_layout.addWidget(self._spacing_widget)
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

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setMinimumWidth(self.sizeHint().width())

    def sizeHint(self):
        return self._main_layout.sizeHint()

    def set_left_padding(self, padding: int):
        self._left_padding = padding
        self._spacing_widget.setFixedWidth(self._left_padding)

    def _on_toggled(self, state):
        if self._icon:
            self._icon.set_selected(state)

        self._label.setProperty("selected", state)
        self._label.style().unpolish(self._label)
        self._label.style().polish(self._label)
        self._label.update()
