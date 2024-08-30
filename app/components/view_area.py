# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGraphicsDropShadowEffect

from pymupdf.utils import get_pixmap
from pymupdf import Identity

from lib import CardWidget, ScrollArea, PixmapLabel


class ViewArea(CardWidget):
    """ViewArea"""

    def __init__(self, path, doc, parent=None):
        super().__init__(parent)

        self.path = path
        self.document = doc
        self.page_count = doc.page_count

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        self.vertical_scroll_area = ScrollArea(self)
        self.vertical_scroll_area.setStyleSheet(
            "border: none; background-color: transparent"
        )
        self.vertical_scroll_area.setWidgetResizable(True)
        self.vertical_scroll_area.horizontalScrollBar().setValue(1900)

        self.vertical_scroll_widget = QWidget()
        self.vertical_page_layout = QVBoxLayout()
        self.vertical_page_layout.setAlignment(Qt.AlignCenter)

        self.vertical_scroll_widget.setLayout(self.vertical_page_layout)
        self.main_layout.addWidget(self.vertical_scroll_widget)
        self.vertical_scroll_area.setWidget(self.vertical_scroll_widget)
        self.main_layout.addWidget(self.vertical_scroll_area)

        self.render_page()

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

            _shadow = QGraphicsDropShadowEffect()
            _shadow.setBlurRadius(15)
            _shadow.setColor(QColor(10, 10, 10, 100))
            _shadow.setOffset(0, 0)
            page_widget.setGraphicsEffect(_shadow)

            del page_pixmap
