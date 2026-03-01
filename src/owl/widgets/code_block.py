from qtpy import QtWidgets, QtCore
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class CodeBlock(QtWidgets.QTextEdit):
    def __init__(self, text: str, parent: QtWidgets.QWidget = None):
        super().__init__(parent)

        self.setStyleSheet(f"""
CodeBlock
{{
    background: transparent;
    color: rgb(220, 220, 220);
}}
""")

        formatter = HtmlFormatter(noclasses=True, style="dracula", nobackground=True)
        html = highlight(text, PythonLexer(), formatter)
        print("html", html)

        self.setHtml(html)
