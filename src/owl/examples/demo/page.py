import owl
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

from .pages import NotificationPage


class MainWindow(owl.Background):
    def __init__(self):
        super().__init__()
        # self.set_effect(owl.GradientCirclesBackgroundEffect())
        self.init_geometry(scale=0.7)
        self.init_ui()

    def init_geometry(self, scale: float = 0.7):
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * scale)
        height = int(screen.height() * scale)
        x = (screen.width() - width) // 2
        y = (screen.height() - height) // 2
        self.setGeometry(x, y, width, height)

    def init_ui(self):
        card = owl.Container()
        card.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        card2 = owl.Container()

        tabs = owl.Tabs(orientation=QtCore.Qt.Orientation.Vertical)
        card.addWidget(tabs)
        tabs.addTab("Notification", owl.Icon("chart-area"))
        tabs.addTab("Tab", owl.Icon("square-chart-gantt"))
        tabs.addTab("Dropdown", owl.Icon("panel-top-open"))
        tabs.addTab("Icon", owl.Icon("image"))
        tabs.addTab("Spinner", owl.Icon("loader-circle"))
        tabs.addTab("Card", owl.Icon("square"))
        tabs.addTab("Codeblock", owl.Icon("code"))

        self.add_widgets(tabs, card2)
        stacked_layout = QtWidgets.QStackedLayout()

        page_container = owl.Container()
        page_container.add_layout(stacked_layout)
        page_container.setMaximumWidth(800)

        page_background = owl.Background(color=owl.Color.WINDOW)
        # page_background.set_effect(owl.GradientCirclesBackgroundEffect())

        page_background.add_widget(page_container)
        page_background.layout.setAlignment(QtCore.Qt.AlignHCenter)
        page_background.layout.setContentsMargins(30, 40, 30, 30)

        card2.add_widget(page_background)

        stacked_layout.addWidget(NotificationPage())
        stacked_layout.addWidget(owl.Button("Tab"))
        stacked_layout.addWidget(QtWidgets.QLabel("Dropdown"))
        stacked_layout.addWidget(QtWidgets.QLabel("Icon"))
        stacked_layout.addWidget(QtWidgets.QLabel("Spinner"))
        stacked_layout.addWidget(QtWidgets.QLabel("Card"))
        stacked_layout.addWidget(QtWidgets.QLabel("Codeblock"))

        tabs.index_changed.connect(lambda index: stacked_layout.setCurrentIndex(index))


def main():
    app = QApplication()
    app.setFont(QtGui.QFont("Open Sans", 10))

    window = MainWindow()
    window.show()
    app.exec()
