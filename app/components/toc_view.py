# coding:utf-8

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget

from lib import (
    qrouter,
    CardWidget,
    FluentIcon,
    SubtitleLabel,
    NavigationInterface,
    HorizontalSeparator,
    TransparentToolButton,
    NavigationItemPosition,
)

from ..components.toc_widget import TocList, TocImage


class TocView(CardWidget):
    """Table of Content View"""

    content_clicked = pyqtSignal(int)

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        self.toc = doc.get_toc()
        self.page_count = doc.page_count

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(10)

        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        self.init_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.title_text = SubtitleLabel("Table of Contents", self)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)

        self.sep = HorizontalSeparator(self)

        if self.toc:
            self.stacked_widget = QStackedWidget(self)
            self.stacked_widget.setContentsMargins(0, 0, 0, 0)
            self.stacked_widget.currentChanged.connect(
                self.on_current_index_changed
            )

            self.navigation = NavigationInterface(
                self, showMenuButton=False, showReturnButton=False
            )

    def init_sub_interface(self, pixmap_list):
        """initialize sub interface"""
        self.toc_image = TocImage(pixmap_list, self.page_count, self)
        self.toc_image.content_clicked.connect(self.on_content_clicked)

        if self.toc:
            self.toc_list = TocList(self.toc, self)
            self.toc_list.content_clicked.connect(self.on_content_clicked)

            self.add_sub_interface(self.toc_list, FluentIcon.MENU)
            self.add_sub_interface(self.toc_image, FluentIcon.PHOTO)
            self.setFixedWidth(350)
        else:
            self.main_layout.addWidget(self.toc_image)
            self.setFixedWidth(300)

    def init_layout(self):
        """initialize layout"""
        self.title_layout.addWidget(self.title_text)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)
        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.sep)
        if self.toc:
            self.content_layout.addWidget(self.navigation)
            self.content_layout.addWidget(self.stacked_widget)
            self.main_layout.addLayout(self.content_layout)

    def add_sub_interface(self, interface, icon, parent=None):
        """add_sub_interface"""
        self.stacked_widget.addWidget(interface)

        routeKey = interface.objectName()
        self.navigation.addItem(
            routeKey=routeKey,
            icon=icon,
            text="",
            onClick=lambda: self.switch_to_interface(interface),
            position=NavigationItemPosition.TOP,
            tooltip="",
            parentRouteKey=parent.objectName() if parent else None,
        )

        if self.stacked_widget.count() == 1:
            self.navigation.setCurrentItem(routeKey)
            qrouter.setDefaultRouteKey(self.stacked_widget, routeKey)
            self.stacked_widget.setCurrentWidget(interface)

    def on_current_index_changed(self, index):
        """on current index changed"""
        widget = self.stacked_widget.widget(index)
        if not widget:
            return

        self.navigation.setCurrentItem(widget.objectName())
        qrouter.push(self.stacked_widget, widget.objectName())

    def on_content_clicked(self, page_count):
        """on content clicked"""
        self.content_clicked.emit(page_count)

    def switch_to_interface(self, interface):
        """switch to interface"""
        self.stacked_widget.setCurrentWidget(interface)
