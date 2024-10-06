# coding:utf-8

from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QColor, QTransform
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QGraphicsDropShadowEffect,
    QApplication,
)
from pymupdf.utils import get_pixmap
from pymupdf import Identity

from lib import (
    CardWidget,
    ScrollArea,
    PixmapLabel,
    toggleTheme,
    InfoBar,
    InfoBarPosition,
)

from ..components.custom_message_box import InfoDialogBox
from ..components.tool_bar import ToolBar
from ..components.toc_view import TocView
from ..components.text_view import TextView


class ViewArea(CardWidget):
    """ViewArea"""

    zoomChanged = pyqtSignal(int)

    def __init__(self, path, doc, parent=None):
        super().__init__(parent)

        self.path = path
        self.document = doc
        self.page_count = doc.page_count
        self.page_widget_list = []
        self.page_pixmap_list = []
        self.page_pixmap_dict = {}
        self.current_page = 1
        self.page_rotation = 0
        self.is_fit_page = False
        self.show_toc_view = False
        self.show_text_view = False
        self.text = ""
        self.html = ""

        # Zoom settings
        self.zoom_level = 100  # Default zoom level in percentage
        self.MIN_ZOOM = 50     # Minimum zoom level
        self.MAX_ZOOM = 200    # Maximum zoom level

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        self.vertical_page_layout = QVBoxLayout()
        self.vertical_page_layout.setAlignment(Qt.AlignCenter)

        self.init_widget()
        self.init_layout()
        self.render_page()

        # Connect zoomChanged signal to update zoom buttons
        self.zoomChanged.connect(self.update_zoom_buttons)

    def init_widget(self):
        """initialize widget"""

        self.tool_bar = ToolBar()
        self.tool_bar.page_count_line_edit.setText(str(self.current_page))
        self.tool_bar.page_count_label.setText(
            f"/ {self.page_count}",
        )
        self.tool_bar.content_button.clicked.connect(
            self.change_toc_view_visibility
        )
        self.tool_bar.more_button.clicked.connect(
            self.change_text_view_visibility
        )
        self.tool_bar.theme_button.clicked.connect(lambda: toggleTheme(True))
        self.tool_bar.info_button.clicked.connect(self.show_info)
        self.tool_bar.prev_page.clicked.connect(self.prev_page)
        self.tool_bar.next_page.clicked.connect(self.next_page)
        self.tool_bar.page_count_line_edit.returnPressed.connect(
            self.go_to_page
        )
        self.tool_bar.zoom_in.clicked.connect(lambda: self.zoom_page(10))
        self.tool_bar.zoom_out.clicked.connect(lambda: self.zoom_page(-10))
        self.tool_bar.fit_page.clicked.connect(self.fit_page)
        self.tool_bar.rotate_page.clicked.connect(self.rotate_page)

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

        self.toc_view = TocView(self.document, self)
        self.toc_view.close_button.clicked.connect(
            self.change_toc_view_visibility
        )
        self.toc_view.content_clicked.connect(self.go_to_page)
        self.toc_view.setVisible(self.show_toc_view)
        self.toc_view.move(10, 74)

        self.text_view = TextView(self)
        self.text_view.close_button.clicked.connect(
            self.change_text_view_visibility
        )
        self.text_view.setVisible(self.show_text_view)

    def init_layout(self):
        """initialize layout"""
        self.main_layout.addWidget(self.tool_bar)
        self.vertical_scroll_widget.setLayout(self.vertical_page_layout)
        self.vertical_scroll_area.setWidget(self.vertical_scroll_widget)
        self.main_layout.addWidget(self.vertical_scroll_area)

    def render_page(self):
        """render page"""
        for i in range(self.page_count):
            page = self.document.load_page(i)
            self.text += page.get_text("text")
            self.html += page.get_text("html")
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
            page_widget.setAlignment(Qt.AlignCenter)
            page_widget.setPixmap(pixmap)
            self.vertical_page_layout.addWidget(page_widget)
            self.page_widget_list.append(page_widget)
            self.page_pixmap_list.append(pixmap)
            self.page_pixmap_dict[page_widget] = pixmap

            # Apply initial zoom
            self.apply_zoom(page_widget)

            _shadow = QGraphicsDropShadowEffect()
            _shadow.setBlurRadius(15)
            _shadow.setColor(QColor(10, 10, 10, 100))
            _shadow.setOffset(0, 0)
            page_widget.setGraphicsEffect(_shadow)

            del page_pixmap

        self.toc_view.init_sub_interface(self.page_pixmap_list)
        self.text_view.init_sub_interface(self.text, self.html)

        # After rendering all pages, update zoom buttons
        self.update_zoom_buttons()

    def apply_zoom(self, page_widget):
        """Apply zoom to a single page widget based on the current zoom level."""
        pixmap = self.page_pixmap_dict[page_widget]
        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * self.zoom_level / 100),
            int(pixmap.height() * self.zoom_level / 100),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        page_widget.setPixmap(scaled_pixmap)

    def zoom_page(self, value):
        """Zoom page with limitations."""
        new_zoom = self.zoom_level + value
        if new_zoom < self.MIN_ZOOM:
            new_zoom = self.MIN_ZOOM
            self.show_tooltip("warning", "Minimum Zoom Reached", f"Cannot zoom out below {self.MIN_ZOOM}%.")
        elif new_zoom > self.MAX_ZOOM:
            new_zoom = self.MAX_ZOOM
            self.show_tooltip("warning", "Maximum Zoom Reached", f"Cannot zoom in above {self.MAX_ZOOM}%.")
        
        if new_zoom != self.zoom_level:
            self.zoom_level = new_zoom
            self.zoomChanged.emit(self.zoom_level)
            self.update_zoom()
        else:
            # Zoom level hasn't changed; no action needed
            pass

    def update_zoom(self):
        """Update all pages with the current zoom level."""
        for page_widget in self.page_widget_list:
            self.apply_zoom(page_widget)

        # Update UI elements if necessary
        self.tool_bar.page_count_line_edit.setText(str(self.current_page))

    def update_zoom_buttons(self):
        """Update the state of zoom buttons based on the current zoom level."""
        can_zoom_in = self.zoom_level < self.MAX_ZOOM
        can_zoom_out = self.zoom_level > self.MIN_ZOOM
        self.tool_bar.set_zoom_buttons_enabled(can_zoom_in, can_zoom_out)

    def fit_page(self):
        """fit page"""
        if self.is_fit_page:
            self.is_fit_page = False
            self.zoom_level = 100  # Reset to default zoom
            self.update_zoom()
            self.tool_bar.fit_page.setChecked(False)
        else:
            # Implement fit to width logic
            self.is_fit_page = True
            viewport_width = self.vertical_scroll_area.viewport().width()
            # Assuming first page represents the size
            pixmap = self.page_pixmap_list[0]
            new_zoom = (viewport_width - 40) / pixmap.width() * 100  # Subtracting margins
            self.zoom_level = int(new_zoom)
            if self.zoom_level > self.MAX_ZOOM:
                self.zoom_level = self.MAX_ZOOM
            elif self.zoom_level < self.MIN_ZOOM:
                self.zoom_level = self.MIN_ZOOM
            self.update_zoom()
            self.tool_bar.fit_page.setChecked(True)

    def rotate_page(self):
        """rotate page"""
        if self.page_rotation != 270:
            self.page_rotation += 90
        else:
            self.page_rotation = 0

        matrix = QTransform()
        matrix.rotate(self.page_rotation)

        for page in self.page_widget_list:
            original_pixmap = self.page_pixmap_dict[page]
            rotated_pixmap = original_pixmap.transformed(
                matrix, Qt.SmoothTransformation
            )
            # Apply zoom after rotation
            scaled_pixmap = rotated_pixmap.scaled(
                int(rotated_pixmap.width() * self.zoom_level / 100),
                int(rotated_pixmap.height() * self.zoom_level / 100),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            page.setPixmap(scaled_pixmap)

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
            self.toc_view.toc_image.set_current_page_card(self.current_page)
            scroll_bar = (
                self.toc_view.toc_image.scroll_area.verticalScrollBar()
            )
            space = self.toc_view.toc_image.page_layout.spacing()
            total_height = int(
                -(self.toc_view.toc_image.scroll_area.height() / 3)
                + self.toc_view.toc_image.page_card_dict[1].height() / 3
            )

            for i in range(self.current_page - 1):
                total_height += self.toc_view.toc_image.page_card_dict[
                    i + 1
                ].height()
                total_height += space
            scroll_bar.setValue(total_height)

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

    def go_to_page(self, page_count=None):
        """go to page"""
        try:
            if not page_count:
                page_count = int(self.tool_bar.page_count_line_edit.text())

            if page_count > self.page_count or page_count <= 0:
                self.tool_bar.page_count_line_edit.setText(
                    str(self.current_page)
                )

            else:
                scroll_bar = self.vertical_scroll_area.verticalScrollBar()
                space = self.vertical_page_layout.spacing()

                total_height = 10
                for i in range(page_count - 1):
                    total_height += self.page_widget_list[i].height()
                    total_height += space
                scroll_bar.setValue(total_height)
                self.current_page = page_count

        except ValueError:
            self.tool_bar.page_count_line_edit.setText(str(self.current_page))

    def show_info(self):
        """show info"""
        dialog = InfoDialogBox(self.path, self.document, self)
        dialog.exec()

    def change_toc_view_visibility(self):
        """change toc view visibility"""
        if self.show_toc_view:
            self.toc_view.setVisible(False)
            self.show_toc_view = False
            self.tool_bar.content_button.setChecked(False)
        else:
            self.toc_view.setVisible(True)
            self.show_toc_view = True
            self.tool_bar.content_button.setChecked(True)

    def change_text_view_visibility(self):
        """change text view visibility"""
        if self.show_text_view:
            self.text_view.setVisible(False)
            self.show_text_view = False
            self.tool_bar.more_button.setChecked(False)
        else:
            self.text_view.setVisible(True)
            self.show_text_view = True
            self.tool_bar.more_button.setChecked(True)

    def resizeEvent(self, event):
        """Handle the resize event"""
        super().resizeEvent(event)

        distance = (
            self.main_layout.getContentsMargins()[1]
            + self.main_layout.getContentsMargins()[3]
            + self.main_layout.spacing()
            + self.tool_bar.height()
        )
        if not distance:
            distance = 85
        self.toc_view.setFixedSize(
            self.toc_view.width(), int(self.height() - distance)
        )

        self.text_view.move(
            int(
                self.width()
                - self.text_view.width()
                - self.main_layout.getContentsMargins()[2]
            ),
            74,
        )
        self.text_view.setFixedSize(
            self.text_view.width(), int(self.height() - distance)
        )

    def show_tooltip(self, tooltip_type: str, title: str, content: str):
        """Show tooltip"""
        if tooltip_type == "success":
            InfoBar.success(
                title=title,
                content=content,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1500,
                parent=self,
            )
        elif tooltip_type == "warning":
            InfoBar.warning(
                title=title,
                content=content,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=1500,
                parent=self,
            )
        elif tooltip_type == "error":
            InfoBar.error(
                title=title,
                content=content,
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=1500,
                parent=self,
            )
