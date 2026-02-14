from owl import Background, Card, Spinner, Icon, EllipsisLabel, CodeBlock, Tabs, Dropdown
import owl
from qtpy import QtWidgets, QtCore, QtGui

app = QtWidgets.QApplication()

window = Background(color=owl.Color.WINDOW)
window.setLayout(QtWidgets.QVBoxLayout())
card = Background()
card.setLayout(QtWidgets.QVBoxLayout())
window.layout().addWidget(card)
window.layout().addWidget(CodeBlock())

window.layout().addWidget(Spinner())
window.layout().addWidget(EllipsisLabel("Hello world foo bar Hello world foo bar Hello world foo bar "))

# tabs = Tabs()
tabs = Tabs(orientation=QtCore.Qt.Orientation.Vertical)
card.layout().addWidget(tabs)
tabs.addTab("foo", Icon("zap"))
tabs.addTab("bar", Icon("album"))
tabs.addTab(
    "hello",
    Icon(file_path=r"/home/parker/Downloads/zap(1).png", file_path_selected=r"/home/parker/Downloads/profile.png"),
    # Icon(file_path=r"/home/parker/Downloads/block.png", file_path_selected=r"/home/parker/Downloads/profile.png"),
)
window.show()
app.exec()
