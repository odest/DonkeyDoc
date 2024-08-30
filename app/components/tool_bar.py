# coding:utf-8

from PyQt5.QtWidgets import QHBoxLayout

from lib import (
    LineEdit,
    CardWidget,
    FluentIcon,
    StrongBodyLabel,
    TransparentToolButton,
    TransparentToggleToolButton,
)


class ToolBar(CardWidget):
    """ToolBar"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        self.content_button = TransparentToggleToolButton(
            FluentIcon.ALIGNMENT, self
        )
        self.main_layout.addWidget(self.content_button)

        self.theme_button = TransparentToolButton(FluentIcon.CONSTRACT, self)
        self.main_layout.addWidget(self.theme_button)
        self.main_layout.addStretch()

        self.prev_page = TransparentToolButton(FluentIcon.PAGE_LEFT, self)
        self.main_layout.addWidget(self.prev_page)

        self.page_count_line_edit = LineEdit(self)
        self.page_count_line_edit.setFixedWidth(48)
        self.main_layout.addWidget(self.page_count_line_edit)
        self.page_count_label = StrongBodyLabel(self)
        self.main_layout.addWidget(self.page_count_label)

        self.next_page = TransparentToolButton(FluentIcon.PAGE_RIGHT, self)
        self.main_layout.addWidget(self.next_page)
        self.main_layout.addStretch()

        self.info_button = TransparentToolButton(FluentIcon.INFO, self)
        self.main_layout.addWidget(self.info_button)
        self.more_button = TransparentToggleToolButton(FluentIcon.FONT, self)
        self.main_layout.addWidget(self.more_button)
