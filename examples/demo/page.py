import owl
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

app = QApplication()

window = owl.Background(owl.Color.WINDOW)
window.setLayout(QtWidgets.QVBoxLayout())
card = owl.Background()
card.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
window.addWidget(card)

# tabs = Tabs()
tabs = owl.Tabs(orientation=QtCore.Qt.Orientation.Vertical)
card.addWidget(tabs)
tabs.addTab("tab", owl.Icon("square-chart-gantt"))
tabs.addTab("dropdown", owl.Icon("panel-top-open"))
tabs.addTab("icon", owl.Icon("image"))
tabs.addTab("spinner", owl.Icon("loader-circle"))
tabs.addTab("card", owl.Icon("square"))
tabs.addTab("codeblock", owl.Icon("code"))

stacked_layout = QtWidgets.QStackedLayout()
card.add_layout(stacked_layout)

stacked_layout.addWidget(QtWidgets.QLabel("Tab"))
stacked_layout.addWidget(QtWidgets.QLabel("Dropdown"))
stacked_layout.addWidget(QtWidgets.QLabel("Icon"))
stacked_layout.addWidget(QtWidgets.QLabel("Spinner"))
stacked_layout.addWidget(QtWidgets.QLabel("Card"))
stacked_layout.addWidget(QtWidgets.QLabel("Codeblock"))

tabs.index_changed.connect(lambda index: stacked_layout.setCurrentIndex(index))

window.show()
app.exec()
