# coding:utf-8

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from lib import (
    CardWidget,
    FluentIcon,
    SubtitleLabel,
    HorizontalSeparator,
    TransparentToolButton,
)

from ..components.toc_widget import TocList


class TocView(CardWidget):
    """Table of Content View"""

    content_clicked = pyqtSignal(int)

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        self.document = doc

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(10)

        self.init_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.title_text = SubtitleLabel("Table of Contents", self)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)

        self.sep = HorizontalSeparator(self)
        self.toc_list = TocList(self.document)
        self.toc_list.content_clicked.connect(self.on_content_clicked)

    def init_layout(self):
        """initialize layout"""
        self.title_layout.addWidget(self.title_text)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)
        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.sep)
        self.main_layout.addWidget(self.toc_list)

    def on_content_clicked(self, page_count):
        """on content clicked"""
        self.content_clicked.emit(page_count)
