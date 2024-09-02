# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget

from lib import (
    qrouter,
    TextEdit,
    CardWidget,
    FluentIcon,
    SubtitleLabel,
    SegmentedWidget,
    HorizontalSeparator,
    TransparentToolButton,
)


class TextView(CardWidget):
    """Text View"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(10)

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        self.init_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.title_text = SubtitleLabel("File Contents", self)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)

        self.sep = HorizontalSeparator(self)

        self.pivot = SegmentedWidget(self)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.currentChanged.connect(
            self.on_current_index_changed
        )

        self.text_area = TextEdit(self)
        self.text_area.setReadOnly(True)
        self.html_area = TextEdit(self)
        self.html_area.setReadOnly(True)

    def init_sub_interface(self, text, html):
        """initialize sub interface"""
        self.text_area.setText(text)
        self.html_area.setHtml(html)

        self.add_sub_interface(self.text_area, "text_area", "Text")
        self.add_sub_interface(self.html_area, "html_area", "Html")
        self.stacked_widget.setCurrentWidget(self.text_area)
        if len(text) > 0:
            self.pivot.setCurrentItem("text_area")
        else:
            self.pivot.setCurrentItem("html_area")
        self.setFixedWidth(350)

    def init_layout(self):
        """initialize layout"""
        self.title_layout.addWidget(self.title_text)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)
        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.sep)
        self.content_layout.addWidget(self.pivot)
        self.content_layout.addWidget(self.stacked_widget)
        self.main_layout.addLayout(self.content_layout)

    def add_sub_interface(self, widget, objectName, title):
        """add sub interface"""
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stacked_widget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=title,
            onClick=lambda: self.stacked_widget.setCurrentWidget(widget),
        )

    def on_current_index_changed(self, index):
        """on current index changed"""
        widget = self.stacked_widget.widget(index)
        if not widget:
            return

        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stacked_widget, widget.objectName())
