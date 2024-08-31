# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from lib import (
    setFont,
    CardWidget,
    ScrollArea,
    FluentIcon,
    SubtitleLabel,
    StrongBodyLabel,
    HorizontalSeparator,
    TransparentToolButton,
)


class TocView(CardWidget):
    """Table of Content View"""

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        self.toc = doc.get_toc()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(10)

        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignLeft)

        self.init_widget()
        self.init_content_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.title_text = SubtitleLabel("Table of Contents", self)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)

        self.sep = HorizontalSeparator(self)

        self.scroll_area = ScrollArea()
        self.scroll_area.setStyleSheet(
            "border: none; background-color: transparent"
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.horizontalScrollBar().setValue(1900)

        self.scroll_widget = QWidget()

    def init_layout(self):
        """initialize layout"""
        self.title_layout.addWidget(self.title_text)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)
        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.sep)
        self.scroll_widget.setLayout(self.content_layout)
        self.main_layout.addWidget(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

    def init_content_widget(self):
        """init content widget"""
        for i in self.toc:
            tab = " " * (i[0] - 1) * 8
            text = f"{tab}{i[1]}"
            base_font_size = 16
            font_size = base_font_size - ((i[0] - 1) * 2)

            self.label = StrongBodyLabel(text, self)
            setFont(self.label, font_size)
            self.content_layout.addWidget(self.label)
