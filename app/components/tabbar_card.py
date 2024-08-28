# coding:utf-8
from PyQt5.QtWidgets import QHBoxLayout

from lib import CardWidget


class TabBarCard(CardWidget):
    """TabBarCard"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMaximumHeight(48)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.setSpacing(12)
