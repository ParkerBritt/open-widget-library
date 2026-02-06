from open_widget_library.dropdown import Dropdown
from open_widget_library.tabs import Tabs
from open_widget_library import Background, Card, Spinner, widget_config
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
tabs.addTab("foo", widget_config.get_icon_pixmap("zap", "white"), widget_config.get_icon_pixmap("zap", "black"))
tabs.addTab("bar", widget_config.get_icon_pixmap("zap", "white"), widget_config.get_icon_pixmap("zap", "black"))
tabs.addTab("hello", widget_config.get_icon_pixmap("zap", "white"), widget_config.get_icon_pixmap("zap", "black"))
window.show()
app.exec()
