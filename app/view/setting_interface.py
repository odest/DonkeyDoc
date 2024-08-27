# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel

from lib import (
    InfoBar,
    setTheme,
    ScrollArea,
    FluentIcon,
    ExpandLayout,
    setThemeColor,
    SettingCardGroup,
    SwitchSettingCard,
    OptionsSettingCard,
    CustomColorSettingCard,
)

from ..common.style_sheet import StyleSheet
from ..common.config import cfg, is_win_11
from ..common.signal_bus import signalBus


class SettingInterface(ScrollArea):
    """Setting interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.resize(1000, 800)
        self.setWidgetResizable(True)
        self.setViewportMargins(0, 80, 0, 20)
        self.setObjectName("SettingInterface")
        # initialize style sheet
        StyleSheet.SETTING_INTERFACE.apply(self)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.init_widget()
        self.init_card_group()
        self.init_layout()
        self.connect_signal_to_slot()

    def init_widget(self):
        """initialize widget"""
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scroll_widget")
        self.setWidget(self.scroll_widget)

        self.expand_layout = ExpandLayout(self.scroll_widget)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.setSpacing(28)

        # setting label
        self.setting_label = QLabel("Settings", self)
        self.setting_label.move(36, 30)
        self.setting_label.setObjectName("setting_label")

    def init_card_group(self):
        """initialize card group"""

        # personalization
        self.personal_group = SettingCardGroup(
            "Personalization", self.scroll_widget
        )
        self.mica_card = SwitchSettingCard(
            FluentIcon.TRANSPARENT,
            "Mica effect",
            "Apply semi transparent to windows and surfaces",
            cfg.micaEnabled,
            self.personal_group,
        )
        self.mica_card.setEnabled(is_win_11())
        self.theme_card = OptionsSettingCard(
            cfg.themeMode,
            FluentIcon.BRUSH,
            "Application theme",
            "Change the appearance of your application",
            texts=["Light", "Dark", "Use system setting"],
            parent=self.personal_group,
        )
        self.theme_color_card = CustomColorSettingCard(
            cfg.themeColor,
            FluentIcon.PALETTE,
            "Theme color",
            "Change the theme color of you application",
            self.personal_group,
        )
        self.zoom_card = OptionsSettingCard(
            cfg.dpiScale,
            FluentIcon.ZOOM,
            "Interface zoom",
            "Change the size of widgets and fonts",
            texts=[
                "100%",
                "125%",
                "150%",
                "175%",
                "200%",
                "Use system setting",
            ],
            parent=self.personal_group,
        )

    def init_layout(self):
        """initialize layout"""
        self.personal_group.addSettingCard(self.mica_card)
        self.personal_group.addSettingCard(self.theme_card)
        self.personal_group.addSettingCard(self.theme_color_card)
        self.personal_group.addSettingCard(self.zoom_card)

        self.expand_layout.addWidget(self.personal_group)

    def show_restart_tooltip(self):
        """show restart tooltip"""
        InfoBar.success(
            "Updated successfully",
            "Configuration takes effect after restart",
            duration=1500,
            parent=self,
        )

    def connect_signal_to_slot(self):
        """connect signal to slot"""
        cfg.appRestartSig.connect(self.show_restart_tooltip)

        # personalization
        self.mica_card.checkedChanged.connect(signalBus.micaEnableChanged)
        self.theme_card.optionChanged.connect(lambda ci: setTheme(cfg.get(ci)))
        self.theme_color_card.colorChanged.connect(lambda c: setThemeColor(c))
