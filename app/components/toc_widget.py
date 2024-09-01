# coding:utf-8

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from lib import TextWrap, NavigationInterface, NavigationItemPosition


class TocList(QWidget):
    """Table of Content List Widget"""

    content_clicked = pyqtSignal(int)

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        self.toc = doc.get_toc()
        self.stack = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.init_widget()
        self.init_content_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""

        self.navigation = NavigationInterface(
            self, showMenuButton=False, showReturnButton=False
        )
        self.navigation.setExpandWidth(300)
        self.navigation.setCollapsible(False)

    def init_layout(self):
        """initialize layout"""
        self.main_layout.addWidget(self.navigation)

    def init_content_widget(self):
        """init content widget"""
        for level, title, page in self.toc:
            interface = QWidget()
            interface.setObjectName(f"{title}:{page}")

            if level > len(self.stack):
                self.stack.append(interface)
            else:
                self.stack = self.stack[:level]
                self.stack.append(interface)

            parent = self.stack[-2] if level > 1 else None

            routeKey = interface.objectName()
            self.navigation.addItem(
                routeKey=routeKey,
                icon="",
                text=TextWrap.wrap(title, 28, False)[0],
                onClick=lambda clicked, i=page: self.content_clicked.emit(i),
                position=NavigationItemPosition.SCROLL,
                tooltip="",
                parentRouteKey=parent.objectName() if parent else None,
            )
