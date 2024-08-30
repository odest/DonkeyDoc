# coding:utf-8

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGraphicsDropShadowEffect

from pymupdf.utils import get_pixmap
from pymupdf import Identity

from lib import CardWidget, ScrollArea, PixmapLabel, toggleTheme
from ..components.tool_bar import ToolBar


class ViewArea(CardWidget):
    """ViewArea"""

    def __init__(self, doc, parent=None):
        super().__init__(parent)

        self.document = doc
        self.page_count = doc.page_count
        self.page_widget_list = []
        self.current_page = 1

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        self.vertical_page_layout = QVBoxLayout()
        self.vertical_page_layout.setAlignment(Qt.AlignCenter)

        self.init_widget()
        self.init_layout()
        self.render_page()

    def init_widget(self):
        """initialize widget"""

        self.tool_bar = ToolBar()
        self.tool_bar.page_count_line_edit.setText(str(self.current_page))
        self.tool_bar.page_count_label.setText(
            f"/ {self.page_count}",
        )
        self.tool_bar.theme_button.clicked.connect(lambda: toggleTheme(True))
        self.tool_bar.prev_page.clicked.connect(self.prev_page)
        self.tool_bar.next_page.clicked.connect(self.next_page)
        self.tool_bar.page_count_line_edit.returnPressed.connect(
            self.go_to_page
        )
        self.main_layout.addWidget(self.tool_bar)

        self.vertical_scroll_area = ScrollArea(self)
        self.vertical_scroll_area.setStyleSheet(
            "border: none; background-color: transparent"
        )
        self.vertical_scroll_area.setWidgetResizable(True)
        self.vertical_scroll_area.horizontalScrollBar().setValue(1900)
        self.vertical_scroll_area.verticalScrollBar().valueChanged.connect(
            self.scroll_page
        )

        self.vertical_scroll_widget = QWidget()

    def init_layout(self):
        """initialize layout"""

        self.vertical_scroll_widget.setLayout(self.vertical_page_layout)
        self.main_layout.addWidget(self.vertical_scroll_widget)
        self.vertical_scroll_area.setWidget(self.vertical_scroll_widget)
        self.main_layout.addWidget(self.vertical_scroll_area)

    def render_page(self):
        """render page"""
        for i in range(self.page_count):
            page = self.document.load_page(i)
            page_pixmap = get_pixmap(page, matrix=Identity, clip=True)
            if page_pixmap.alpha:
                image_format = QImage.Format.Format_RGBA8888
            else:
                image_format = QImage.Format.Format_RGB888
            page_image = QImage(
                page_pixmap.samples,
                page_pixmap.w,
                page_pixmap.h,
                page_pixmap.stride,
                image_format,
            )
            pixmap = QPixmap()
            pixmap.convertFromImage(page_image)

            page_widget = PixmapLabel(self)
            page_widget.setPixmap(pixmap)
            self.vertical_page_layout.addWidget(page_widget)
            self.page_widget_list.append(page_widget)

            _shadow = QGraphicsDropShadowEffect()
            _shadow.setBlurRadius(15)
            _shadow.setColor(QColor(10, 10, 10, 100))
            _shadow.setOffset(0, 0)
            page_widget.setGraphicsEffect(_shadow)

            del page_pixmap

    def scroll_page(self):
        """scroll page"""
        viewport_rect = self.vertical_scroll_area.viewport().rect()
        max_visible_area = 0

        for page in self.page_widget_list:
            page_rect = self.vertical_scroll_area.viewport().mapFromGlobal(
                page.mapToGlobal(page.rect().topLeft())
            )
            page_visible_rect = QRect(page_rect, page.size()).intersected(
                viewport_rect
            )
            visible_area = (
                page_visible_rect.width() * page_visible_rect.height()
            )

            if visible_area > max_visible_area:
                max_visible_area = visible_area
                self.current_page = self.page_widget_list.index(page) + 1

        if self.current_page:
            self.tool_bar.page_count_line_edit.setText(str(self.current_page))

    def prev_page(self):
        """prev page"""
        if not (self.current_page > self.page_count or self.current_page <= 1):
            self.current_page -= 1
            self.tool_bar.page_count_line_edit.setText(str(self.current_page))
            self.go_to_page()

    def next_page(self):
        """next page"""
        if not (self.current_page >= self.page_count or self.current_page < 1):
            self.current_page += 1
            self.tool_bar.page_count_line_edit.setText(str(self.current_page))
            self.go_to_page()

    def go_to_page(self):
        """go to page"""
        try:
            count = int(self.tool_bar.page_count_line_edit.text())

            if count > self.page_count or count <= 0:
                self.tool_bar.page_count_line_edit.setText(
                    str(self.current_page)
                )

            else:
                scroll_bar = self.vertical_scroll_area.verticalScrollBar()
                space = self.vertical_page_layout.spacing()

                total_height = 10
                for i in range(count - 1):
                    total_height += self.page_widget_list[i].height()
                    total_height += space
                scroll_bar.setValue(total_height)

        except ValueError:
            self.tool_bar.page_count_line_edit.setText(str(self.current_page))
