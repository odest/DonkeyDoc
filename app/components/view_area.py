# coding:utf-8

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QImage, QPixmap, QColor, QTransform
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGraphicsDropShadowEffect

from pymupdf.utils import get_pixmap
from pymupdf import Identity

from lib import CardWidget, ScrollArea, PixmapLabel, toggleTheme

from ..components.custom_message_box import InfoDialogBox
from ..components.tool_bar import ToolBar


class ViewArea(CardWidget):
    """ViewArea"""

    def __init__(self, path, doc, parent=None):
        super().__init__(parent)

        self.path = path
        self.document = doc
        self.page_count = doc.page_count
        self.page_widget_list = []
        self.page_pixmap_dict = {}
        self.current_page = 1
        self.page_rotation = 0
        self.is_fit_page = False

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
        self.tool_bar.info_button.clicked.connect(self.show_info)
        self.tool_bar.prev_page.clicked.connect(self.prev_page)
        self.tool_bar.next_page.clicked.connect(self.next_page)
        self.tool_bar.page_count_line_edit.returnPressed.connect(
            self.go_to_page
        )
        self.tool_bar.zoom_in.clicked.connect(lambda: self.zoom_page(50))
        self.tool_bar.zoom_out.clicked.connect(lambda: self.zoom_page(-50))
        self.tool_bar.fit_page.clicked.connect(self.fit_page)
        self.tool_bar.rotate_page.clicked.connect(self.rotate_page)
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
            self.page_pixmap_dict[page_widget] = pixmap

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

    def zoom_page(self, value):
        """zoom page"""
        for page in self.page_widget_list:
            page_width = page.width()
            page_height = page.height()
            aspect_ratio = page_height / page_width
            new_height = page_height + value
            new_width = int(new_height / aspect_ratio)
            page.setFixedSize(new_width, new_height)

    def fit_page(self):
        """fit page"""
        if self.is_fit_page:
            self.is_fit_page = False
            scroll_area_height = self.vertical_scroll_area.height()
            for page in self.page_widget_list:
                page_width = page.width()
                page_height = page.height()
                aspect_ratio = page_width / page_height
                new_height = scroll_area_height
                new_width = int(new_height * aspect_ratio)
                page.setFixedSize(new_width, new_height)
        else:
            self.is_fit_page = True
            scroll_area_width = self.vertical_scroll_area.width()
            for page in self.page_widget_list:
                page_width = page.width()
                page_height = page.height()
                aspect_ratio = page_height / page_width
                new_width = scroll_area_width - 20
                new_height = int(new_width * aspect_ratio)
                page.setFixedSize(new_width, new_height)

    def rotate_page(self):
        """rotate page"""
        if self.page_rotation != 270:
            self.page_rotation += 90
        else:
            self.page_rotation = 0

        matrix = QTransform()
        matrix.rotate(self.page_rotation)

        for page in self.page_widget_list:
            rotated_pixmap = self.page_pixmap_dict[page].transformed(
                matrix, Qt.TransformationMode.SmoothTransformation
            )
            page.setPixmap(rotated_pixmap)

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

    def show_info(self):
        """show info"""
        dialog = InfoDialogBox(self.path, self.document, self)
        dialog.exec()
