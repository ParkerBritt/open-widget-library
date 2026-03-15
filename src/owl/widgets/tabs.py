from __future__ import annotations
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
            self._button_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        else:
            self._button_layout = QtWidgets.QVBoxLayout(self)
            self._button_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self._button_layout.setContentsMargins(0, 0, 0, 0)
        self._button_group = QtWidgets.QButtonGroup()
        self._button_group.setExclusive(True)
        self._button_padding = (0, 0, 0, 0)
        self._button_group.idClicked.connect(self._on_id_clicked)

        self._overlay = TabOverlay(self)

        self.overlay_anim = QtCore.QPropertyAnimation(self._overlay, b"bubbleRect")
        self.overlay_anim.setDuration(300)
        self.overlay_anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

    def _on_id_clicked(self, id):
        index = self._index_by_button_id[id]
        self.index_changed.emit(index)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._overlay.setGeometry(self.rect())
        self._place_underline()

    def add_tab(self, name: str, icon: Icon = None) -> int:
        new_button = TabButton(name, icon)

        if self._orientation is QtCore.Qt.Orientation.Vertical:
            button_width = new_button.sizeHint().width()
            if self._largest_button_width < button_width:
                self._largest_button_width = button_width
                self.setMaximumWidth(self._largest_button_width * 2)
        else:
            new_button.setSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum)

        new_button.setCheckable(True)
        new_button.clicked.connect(lambda: self.onButtonPressed(new_button))

        button_index = len(self._button_group.buttons())

        self._button_group.addButton(new_button)
        self._button_layout.addWidget(new_button)

        button_id = self._button_group.id(new_button)
        self._index_by_button_id[button_id] = button_index

        self._overlay.set_buttons(self._button_group.buttons())
        self._overlay.raise_()

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
        self._overlay.bubbleRect = self._bubble_position_for(button)

    def onButtonPressed(self, button):
        if self.overlay_anim.state() == QtCore.QAbstractAnimation.Running:
            self.overlay_anim.stop()

        self.overlay_anim.setStartValue(self._overlay.bubbleRect)
        self.overlay_anim.setEndValue(self._bubble_position_for(button))

        self.overlay_anim.start()

        self._last_selected_button = button


class TabButton(QtWidgets.QPushButton):
    def __init__(self, name: str, icon: Icon = None):
        super().__init__()

        self._name = name
        self._icon = icon
        self._left_padding = 5
        self._right_padding = 5

        self._init_layout()

    def _init_layout(self):
        self._label = QtWidgets.QLabel(self._name)

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self._left_spacing_widget = QtWidgets.QWidget()
        self._left_spacing_widget.setFixedWidth(self._left_padding)
        self._main_layout.addWidget(self._left_spacing_widget)
        self._main_layout.setContentsMargins(0, 4, 0, 4)
        self._main_layout.setAlignment(QtCore.Qt.AlignLeft)
        if self._icon:
            self._main_layout.addWidget(self._icon)
        self._main_layout.addWidget(self._label)
        self._right_spacing_widget = QtWidgets.QWidget()
        self._right_spacing_widget.setFixedWidth(self._right_padding)
        self._main_layout.addWidget(self._right_spacing_widget)

        self.setStyleSheet("""
        QPushButton
        {
            background: transparent;
            border: none;
            color: white;
            border-radius: 8px;
        }
        QPushButton:hover
        {
            background: rgba(255,255,255,0.1);
        }
        QPushButton QLabel
        {
            color: white;
        }
        """)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setMinimumWidth(self.sizeHint().width())

    def sizeHint(self):
        return self._main_layout.sizeHint()

    def set_left_padding(self, padding: int):
        self._left_padding = padding
        self._left_spacing_widget.setFixedWidth(self._left_padding)

class TabOverlay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._bubble_rect = QtCore.QRect()
        self._buttons = []
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAutoFillBackground(False)

    @QtCore.Property(QtCore.QRect)
    def bubbleRect(self):
        return self._bubble_rect

    @bubbleRect.setter
    def bubbleRect(self, rect):
        self._bubble_rect = rect
        self.update()

    def set_buttons(self, buttons):
        self._buttons = buttons

    def paintEvent(self, event):
        if self._bubble_rect.isEmpty():
            return
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self._bubble_rect), 10, 10)
        painter.setClipPath(path)

        painter.setBrush(QtGui.QColor("white"))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(QtCore.QRectF(self._bubble_rect), 10, 10)

        painter.setPen(QtGui.QColor("black"))
        for button in self._buttons:
            if button._icon:
                icon = button._icon
                icon_pos = icon.mapTo(self.parent(), QtCore.QPoint(0, 0))
                button._icon.render_selected(painter, QtCore.QRect(icon_pos, icon.size()))

            label = button._label
            label_pos = label.mapTo(self.parent(), QtCore.QPoint(0, 0))
            label_rect = QtCore.QRect(label_pos, label.size())
            painter.setFont(label.font())
            painter.drawText(label_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, label.text())

        painter.end()
