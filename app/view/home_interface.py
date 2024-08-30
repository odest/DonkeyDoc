# coding:utf-8
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from lib import (
    TabBar,
    InfoBar,
    qrouter,
    FluentIcon,
    CardWidget,
    InfoBarPosition,
    PrimaryPushButton,
    TabCloseButtonDisplayMode,
)

from ..common.style_sheet import StyleSheet
from ..components.drop_card import DropCard
from ..components.view_area import ViewArea
from ..components.tabbar_card import TabBarCard
from ..utils.file_validation import validate_file


class HomeInterface(QWidget):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("HomeInterface")
        # initialize style sheet
        StyleSheet.HOME_INTERFACE.apply(self)

        self.show_drop_card = True
        self.show_tab_bar_card = False
        self.show_stacked_widget = False

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.init_widget()
        self.init_layout()
        self.update_visibility()

    def init_widget(self):
        """initialize widget"""
        self.tab_bar_card = TabBarCard()

        self.tab_bar = TabBar(self)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabShadowEnabled(True)
        self.tab_bar.setCloseButtonDisplayMode(
            TabCloseButtonDisplayMode.ON_HOVER
        )
        self.tab_bar.setAddButtonVisible(False)
        self.tab_bar.setTabMaximumWidth(200)
        self.tab_bar.tabCloseRequested.connect(self.remove_tab)

        self.add_button = PrimaryPushButton(
            "Add Files", self, FluentIcon.DICTIONARY_ADD
        )
        self.add_button.clicked.connect(self.select_file)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget.currentChanged.connect(
            self.on_current_index_changed
        )

        self.drop_card = DropCard()
        self.drop_card.select_signal.connect(self.add_file)
        self.drop_card.tooltip_signal.connect(self.show_tooltip)

    def init_layout(self):
        """initialize layout"""
        self.main_layout.addWidget(self.tab_bar_card)
        self.tab_bar_card.main_layout.addWidget(self.tab_bar)
        self.tab_bar_card.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.drop_card)

    def update_visibility(self):
        """update visibility"""
        self.drop_card.setVisible(self.show_drop_card)
        self.tab_bar_card.setVisible(self.show_tab_bar_card)
        self.stacked_widget.setVisible(self.show_stacked_widget)

    def add_file(self, path):
        """add file"""
        doc, state, tooltip_type, title, content = validate_file(self, path)
        self.show_tooltip(tooltip_type, title, content)

        if not state:
            return

        file_name = os.path.basename(path)
        if file_name in self.tab_bar.itemMap:
            self.tab_bar.setCurrentTab(file_name)
            qrouter.push(self.stacked_widget, file_name)
            self.show_drop_card = False
            self.show_stacked_widget = True
            self.update_visibility()
            self.show_tooltip(
                "warning",
                f"{file_name} already added",
                "",
            )
            return

        view_area = ViewArea(doc)
        self.add_sub_interface(view_area, file_name, file_name)

        self.show_drop_card = False
        self.show_tab_bar_card = True
        self.show_stacked_widget = True
        self.update_visibility()

    def add_sub_interface(self, widget, object_name, text):
        """add sub interface"""
        widget.setObjectName(object_name)
        self.stacked_widget.addWidget(widget)
        self.tab_bar.addTab(
            routeKey=object_name,
            text=text,
            icon=FluentIcon.DOCUMENT,
            onClick=lambda: self.on_sub_interface_clicked(widget),
        )
        self.tab_bar.setCurrentTab(widget.objectName())
        qrouter.push(self.stacked_widget, widget.objectName())
        self.stacked_widget.setCurrentWidget(widget)

    def select_file(self):
        """select file"""
        self.show_drop_card = True
        self.show_stacked_widget = False
        self.update_visibility()

    def remove_tab(self, index):
        """remove tab"""
        item = self.tab_bar.tabItem(index)
        widget = self.findChild(CardWidget, item.routeKey())
        self.tab_bar.removeTab(index)
        self.stacked_widget.removeWidget(widget)
        widget.deleteLater()

        if not len(self.tab_bar.items):
            self.show_drop_card = True
            self.show_tab_bar_card = False
            self.show_stacked_widget = False
            self.update_visibility()

    def on_current_index_changed(self, index):
        """on current index changed"""
        widget = self.stacked_widget.widget(index)
        if not widget:
            return

        self.tab_bar.setCurrentTab(widget.objectName())
        qrouter.push(self.stacked_widget, widget.objectName())
        self.show_drop_card = False
        self.show_stacked_widget = True
        self.update_visibility()

    def on_sub_interface_clicked(self, widget):
        """on sub interface clicked"""
        self.stacked_widget.setCurrentWidget(widget)
        self.show_drop_card = False
        self.show_stacked_widget = True
        self.update_visibility()

    def show_tooltip(self, tooltip_type: str, title: str, content: str):
        """show tooltip"""
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
