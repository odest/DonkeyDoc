# coding:utf-8

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from lib import (
    TextWrap,
    themeColor,
    CardWidget,
    ImageLabel,
    ScrollArea,
    StrongBodyLabel,
    NavigationInterface,
    NavigationItemPosition,
)


class TocList(QWidget):
    """Table of Content List Widget"""

    content_clicked = pyqtSignal(int)

    def __init__(self, toc, parent=None):
        super().__init__(parent)
        self.setObjectName("TocList")

        self.toc = toc
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
        self.navigation.setExpandWidth(280)
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


class TocImage(QWidget):
    """Table of Content Image Widget"""

    content_clicked = pyqtSignal(int)

    def __init__(self, pixmap_list, page_count, parent=None):
        super().__init__(parent)
        self.setObjectName("TocImage")

        self.pixmap_list = pixmap_list
        self.page_count = page_count
        self.current_page = None
        self.page_card_dict = {}

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(10)

        self.page_layout = QVBoxLayout()
        self.page_layout.setAlignment(Qt.AlignCenter)

        self.init_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.scroll_area = ScrollArea(self)
        self.scroll_area.setStyleSheet(
            "border: none; background-color: transparent"
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.horizontalScrollBar().setValue(1900)

        self.scroll_widget = QWidget()

        for i in range(self.page_count):
            page_card = PageCard(self.pixmap_list[i], i + 1)
            page_card.clicked.connect(self.on_page_card_clicked)
            page_card.setStyleSheet(
                "background: transparent; border-radius: 5px;"
            )
            self.page_card_dict[i + 1] = page_card
            self.page_layout.addWidget(page_card)

        self.set_current_page_card(1)

    def init_layout(self):
        """initialize layout"""
        self.scroll_widget.setLayout(self.page_layout)
        self.main_layout.addWidget(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

    def on_page_card_clicked(self):
        """on page card clicked"""
        clicked_page = self.sender()
        self.content_clicked.emit(clicked_page.page_count)

        if self.current_page:
            self.current_page.setStyleSheet(
                "background: transparent; border-radius: 5px;"
            )

        clicked_page.setStyleSheet(
            f"background: rgba{themeColor().getRgb()}; border-radius: 5px;"
        )
        self.current_page = clicked_page

    def set_current_page_card(self, page_count):
        """set current page card"""
        if self.current_page:
            self.current_page.setStyleSheet(
                "background: transparent; border-radius: 5px;"
            )

        self.page_card_dict[page_count].setStyleSheet(
            f"background: rgba{themeColor().getRgb()}; border-radius: 5px;"
        )
        self.current_page = self.page_card_dict[page_count]


class PageCard(CardWidget):
    """Page Card Widget"""

    def __init__(self, pixmap, page_count, parent=None):
        super().__init__(parent)
        self.setObjectName(f"PageCard-{page_count}")

        self.page_count = page_count

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setAlignment(Qt.AlignCenter)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)

        self.page_image_label = ImageLabel(pixmap, self)
        self.page_image_label.setBorderRadius(5, 5, 5, 5)
        self.page_image_label.scaledToWidth(150)
        self.main_layout.addWidget(self.page_image_label)

        self.page_count_label = StrongBodyLabel(str(page_count), self)
        self.bottom_layout.addWidget(self.page_count_label)
        self.main_layout.addLayout(self.bottom_layout)
