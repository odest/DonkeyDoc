# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from lib import CardWidget, StrongBodyLabel


class ViewArea(CardWidget):
    """ViewArea"""

    def __init__(self, item, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        self.selected_file_text = StrongBodyLabel(item, self)
        self.main_layout.addWidget(self.selected_file_text)
