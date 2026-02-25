import owl
from PySide6 import QtCore, QtGui, QtWidgets


class NotificationPage(owl.Background):
    def __init__(self):
        super().__init__(owl.Color.WINDOW)
        # self.setGraphicStyle(self.GraphicStyle.BLURRED_CIRCLES)

        self.add_widget(QtWidgets.QLabel("test"))
