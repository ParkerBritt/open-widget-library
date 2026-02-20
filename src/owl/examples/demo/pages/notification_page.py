import owl
from PySide6 import QtCore, QtGui, QtWidgets

class NotificationPage(owl.Background):
    def __init__(self):
        super().__init__(owl.Color.WINDOW)

        self.add_widget(QtWidgets.QLabel("test"))
