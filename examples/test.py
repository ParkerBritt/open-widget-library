from open_widget_library.dropdown import Dropdown
from open_widget_library.tabs import Tabs
from open_widget_library import Background, Card, Spinner
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

app = QApplication()

window = Background()
window.setLayout(QtWidgets.QVBoxLayout())
card = Card()
card.setLayout(QtWidgets.QVBoxLayout())
window.layout().addWidget(card)

window.layout().addWidget(Spinner())

tabs = Tabs()
card.layout().addWidget(tabs)
tabs.addTab("foo")
tabs.addTab("bar")
tabs.addTab("hello")
window.show()
app.exec()
