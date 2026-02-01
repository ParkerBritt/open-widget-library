from pathlib import Path
from qtpy import QtWidgets, QtCore, QtGui
border_radius = 10;

class WidgetConfig():
    def __init__(self):
        self._icons = {}
        self._PACKAGE_ROOT = Path(__file__).resolve().parent
        self._ICONS_DIR = self._PACKAGE_ROOT / "resources" / "icons" / "lucide"

    @property
    def stylesheet(self):
        style_string = """
    QWidget
    {
        border
    }
    """
        return style_string


    def get_icon(self, icon_name):
        icon = self._icons.get(icon_name)
        if not icon:
            icon = QtGui.QIcon(str(self._ICONS_DIR / icon_name))

        return icon

widget_config = WidgetConfig()
