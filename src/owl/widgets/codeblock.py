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
        formatted_text = "\n".join([f"{i} {line}" for i, line in enumerate(text.splitlines())])

        formatter = HtmlFormatter(noclasses=True, style="dracula", nobackground=True)
        html = highlight(formatted_text, PythonLexer(), formatter)

        self.setHtml(html)
