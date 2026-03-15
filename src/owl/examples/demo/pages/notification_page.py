import owl
from PySide6 import QtCore, QtGui, QtWidgets


class NotificationPage(owl.Container):
    def __init__(self):
        super().__init__()
        self.set_layout_direction(self.TopToBottom)
        # self.set_size_policy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        heading = owl.Label("Notification").set_heading(1)
        self.add_widget(heading)
        # self.add_widget(owl.Label("Toast Notification").set_heading(3))
        self.add_spacing(10)
        self.add_widget(owl.Label(owl.lorem_ipsum(2)).set_text_block())

        self.add_spacing(40)

        tabs = owl.Tabs()
        tabs.add_tab("Preview")
        tabs.add_tab("Code")
        tab_background = owl.Background()
        tab_background.add_widget(tabs)
        tab_background.set_margins(4)
        tab_background.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.add_widget(tab_background)


        preview_background = owl.Background(color=owl.Color.WINDOW)
        self.background = preview_background
        # preview_background.set_effect(owl.BackdropBlur(notification_button))
        preview_background.set_effect(owl.DotMatrixBackgroundEffect())
        preview_background.setFixedHeight(250)
        # preview_background.setGraphicStyle(preview_background.GraphicStyle.BLURRED_CIRCLES)

        codeblock_background = owl.Background().add_widget(owl.CodeBlock("""import owl

notification_button = owl.Button("Test Notify").fill_width(False)
notification_button.clicked.connect(
    lambda: owl.ToastNotification(self.window(), "test").notify()
)
"""))
        codeblock_background.setFixedHeight(250)

        stacked_widget = QtWidgets.QStackedWidget()
        stacked_widget.addWidget(preview_background)
        stacked_widget.addWidget(codeblock_background)
        self.add_widget(stacked_widget)
        tabs.index_changed.connect(lambda index: stacked_widget.setCurrentIndex(index))

        notification_button = owl.Button("Test Notify").fill_width(False)
        notification_button.clicked.connect(
            lambda: owl.ToastNotification(self.window(), "test").notify()
        )
        preview_background.add_widget(notification_button)

        self.add_widget(owl.Label(owl.lorem_ipsum(3)).set_text_block())


        self.set_alignment(notification_button, QtCore.Qt.AlignHCenter)
        self.add_stretch()
