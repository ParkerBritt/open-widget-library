# For raising missing qt bindings exception early
from qtpy import QtWidgets

from .background import Background
from .card import Card
from .spinner import Spinner
from .widget_config import widget_config
from .icon import Icon
from .ellipsis_label import EllipsisLabel


def main() -> None:
    print("Hello from open-widget-library!")
