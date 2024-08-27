# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from lib import DisplayLabel


class HomeInterface(QWidget):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("home_interface")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.display_text = DisplayLabel("Home Interface")
        self.main_layout.addWidget(self.display_text)
