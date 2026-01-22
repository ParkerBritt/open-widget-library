border_radius = 10;

class WidgetConfig():
    @property
    def stylesheet(self):
        style_string = """
    QWidget
    {
        border
    }
    """
        return style_string
