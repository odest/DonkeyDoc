# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from lib import InfoBar, InfoBarPosition

from ..common.style_sheet import StyleSheet
from ..components.drop_card import DropCard


class HomeInterface(QWidget):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("HomeInterface")
        # initialize style sheet
        StyleSheet.HOME_INTERFACE.apply(self)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.drop_card = DropCard()
        self.drop_card.tooltip_signal.connect(self.show_tooltip)
        self.main_layout.addWidget(self.drop_card)

    def show_tooltip(self, tooltip_type: str, title: str, content: str):
        """show tooltip"""
        if tooltip_type == "success":
            InfoBar.success(
                title=title,
                content=content,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1500,
                parent=self,
            )
        elif tooltip_type == "warning":
            InfoBar.warning(
                title=title,
                content=content,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1500,
                parent=self,
            )
