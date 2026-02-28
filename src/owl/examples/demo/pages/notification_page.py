import owl
from PySide6 import QtCore, QtGui, QtWidgets


class NotificationPage(owl.Container):
    def __init__(self):
        super().__init__()
        self.set_layout_direction(self.TopToBottom)
        # self.setGraphicStyle(self.GraphicStyle.BLURRED_CIRCLES)

        self.add_widget(owl.Label("Notification").set_heading(1))
        self.add_widget(owl.Label("Toast Notification").set_heading(3))
        self.add_widget(QtWidgets.QLabel("test"))
