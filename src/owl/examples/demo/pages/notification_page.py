import owl
from PySide6 import QtCore, QtGui, QtWidgets


class NotificationPage(owl.Container):
    def __init__(self):
        super().__init__()
        self.set_layout_direction(self.TopToBottom)
        # self.setGraphicStyle(self.GraphicStyle.BLURRED_CIRCLES)

        self.add_widget(owl.Label("Notification").set_heading(1))
        # self.add_widget(owl.Label("Toast Notification").set_heading(3))
        self.add_spacing(10)
        self.add_widget(
            owl.Label(
                "The notification widget can be used in a range of function for various purposes. Lorum ipsum"
            )
        )

        notification_button = owl.Button("Notify").fill_width(False)
        notification_button.clicked.connect(
            lambda: owl.ToastNotification(self.window(), "test").notify()
        )
        self.add_widget(notification_button)
