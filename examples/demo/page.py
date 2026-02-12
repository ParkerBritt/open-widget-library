import owl
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

app = QApplication()

window = owl.Background(owl.Color.WINDOW)
window.setLayout(QtWidgets.QVBoxLayout())
card = owl.Background()
# card.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
window.addWidget(card)

# tabs = Tabs()
tabs = owl.Tabs(orientation=QtCore.Qt.Orientation.Vertical)
card.addWidget(tabs)
tabs.addTab("tab", owl.Icon("square-chart-gantt"))
tabs.addTab("dropdown", owl.Icon("panel-top-open"))
tabs.addTab("icon", owl.Icon("image"))
tabs.addTab("spinner", owl.Icon("loader-circle"))
tabs.addTab("card", owl.Icon("square"))
window.show()
app.exec()
