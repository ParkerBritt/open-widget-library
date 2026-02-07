from open_widget_library.dropdown import Dropdown
from open_widget_library.tabs import Tabs
from open_widget_library import Background, Card, Spinner, widget_config, Icon
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

app = QApplication()

window = Background()
window.setLayout(QtWidgets.QVBoxLayout())
card = Card()
card.setLayout(QtWidgets.QVBoxLayout())
window.layout().addWidget(card)

window.layout().addWidget(Spinner())

# tabs = Tabs()
tabs = Tabs(orientation=QtCore.Qt.Orientation.Vertical)
card.layout().addWidget(tabs)
tabs.addTab("foo", Icon("zap"))
tabs.addTab("bar", Icon("zap"))
tabs.addTab(
    "hello",
    Icon(file_path=r"/home/parker/Downloads/block.png", file_path_selected=r"/home/parker/Downloads/profile.png"),
)
window.show()
app.exec()
