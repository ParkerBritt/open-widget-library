from open_widget_library.dropdown import Dropdown
from open_widget_library.tabs import Tabs
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

app = QApplication()

window = QtWidgets.QWidget()
window.setLayout(QtWidgets.QVBoxLayout())
window.layout().addWidget(QtWidgets.QLabel("HELLOWORLD"))
tabs = Tabs()
tabs.addTab("foo")
tabs.addTab("bar")
tabs.addTab("hello")
window.layout().addWidget(tabs)
window.show()
app.exec()
