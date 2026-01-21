from open_widget_library.dropdown import Dropdown
from open_widget_library.tabs import Tabs
from open_widget_library import Background
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

app = QApplication()

window = Background()
window.setLayout(QtWidgets.QVBoxLayout())
window.layout().addWidget(QtWidgets.QLabel("HELLOWORLD"))
tabs = Tabs()
tabs.addTab("foo")
tabs.addTab("bar")
tabs.addTab("hello")
window.layout().addWidget(tabs)
window.show()
app.exec()
