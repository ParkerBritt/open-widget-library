import owl
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore, QtGui, QtWidgets

from .pages import NotificationPage


def main():
    app = QApplication()
    app.setFont(QtGui.QFont("Open Sans", 10))

    window = owl.Background()
    # window.setGraphicStyle(window.GraphicStyle.BLURRED_CIRCLES)

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

    window.add_widgets(tabs, card2)
    stacked_layout = QtWidgets.QStackedLayout()

    page_background = owl.Background(color=owl.Color.WINDOW)
    card2.add_widget(page_background)
    page_background.add_layout(stacked_layout)

    stacked_layout.addWidget(NotificationPage())
    stacked_layout.addWidget(QtWidgets.QLabel("Tab"))
    stacked_layout.addWidget(QtWidgets.QLabel("Dropdown"))
    stacked_layout.addWidget(QtWidgets.QLabel("Icon"))
    stacked_layout.addWidget(QtWidgets.QLabel("Spinner"))
    stacked_layout.addWidget(QtWidgets.QLabel("Card"))
    stacked_layout.addWidget(QtWidgets.QLabel("Codeblock"))

    tabs.index_changed.connect(lambda index: stacked_layout.setCurrentIndex(index))

    window.show()
    app.exec()
