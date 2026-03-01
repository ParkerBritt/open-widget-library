import owl
from PySide6 import QtCore, QtGui, QtWidgets


class NotificationPage(owl.Container):
    def __init__(self):
        super().__init__()
        self.set_layout_direction(self.TopToBottom)
        # self.set_size_policy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.add_widget(owl.Label("Notification").set_heading(1))
        # self.add_widget(owl.Label("Toast Notification").set_heading(3))
        self.add_spacing(10)
        self.add_widget(owl.Label(owl.lorem_ipsum(2)).set_text_block())

        notification_button = owl.Button("Test Notify").fill_width(False)
        notification_button.clicked.connect(
            lambda: owl.ToastNotification(self.window(), "test").notify()
        )
        self.add_spacing(40)
        preview_background = owl.Background(color=owl.Color.WINDOW)
        preview_background.setFixedHeight(250)
        # preview_background.setGraphicStyle(preview_background.GraphicStyle.BLURRED_CIRCLES)
        self.add_widget(preview_background)

        preview_background.add_widget(notification_button)

        self.add_widget(owl.CodeBlock("""import owl

notification_button = owl.Button("Test Notify").fill_width(False)
notification_button.clicked.connect(
    lambda: owl.ToastNotification(self.window(), "test").notify()
)
"""))
        self.set_alignment(notification_button, QtCore.Qt.AlignHCenter)
        self.add_stretch()
