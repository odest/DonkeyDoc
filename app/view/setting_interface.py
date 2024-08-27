# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from lib import ExpandLayout, ScrollArea

from ..common.style_sheet import StyleSheet


class SettingInterface(ScrollArea):
    """Setting interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.resize(1000, 800)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 80, 0, 20)
        self.setObjectName("SettingInterface")
        # initialize style sheet
        StyleSheet.SETTING_INTERFACE.apply(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.init_widget()

    def init_widget(self):
        """initialize widget"""
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scroll_widget")
        self.setWidget(self.scroll_widget)

        self.expand_layout = ExpandLayout(self.scroll_widget)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.setSpacing(28)

        # setting label
        self.setting_label = QLabel("Settings", self)
        self.setting_label.move(36, 30)
        self.setting_label.setObjectName("setting_label")
