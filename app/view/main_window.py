# coding: utf-8
import os

from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtWidgets import QApplication

from lib import (
    FluentWindow,
    SplashScreen,
    FluentIcon,
    NavigationItemPosition,
    MessageBox,
)
from ..utils.version_manager import VersionManager
from .home_interface import HomeInterface
from .setting_interface import SettingInterface
from ..common.signal_bus import signalBus
from ..common.config import cfg
from ..common.setting import RELEASE_URL, APP_NAME
from ..common import resource


class MainWindow(FluentWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.version_manager = VersionManager()
        self.init_window()
        self.init_interface()
        self.init_navigation()
        self.connect_signal_to_slot()
        self.splash_screen.finish()

        # check for updates
        if cfg.get(cfg.checkUpdateAtStartUp):
            self.check_update(True)

    def init_interface(self):
        """Initialize the interfaces"""
        self.home_interface = HomeInterface(self)
        self.settings_interface = SettingInterface(self)

    def init_navigation(self):
        """Add navigation items"""
        self.addSubInterface(self.home_interface, FluentIcon.HOME, "Home")
        self.addSubInterface(
            self.settings_interface,
            FluentIcon.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )

    def init_window(self):
        """Initialize the main window properties and display the splash screen."""
        self.resize(970, 790)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(":/gallery/images/logo.png"))
        self.setWindowTitle("DonkeyDoc")

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(106, 106))
        self.splash_screen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(
            int(w // 2 - self.width() // 2), int(h // 2 - self.height() // 2)
        )
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        """Handle the resize event"""
        super().resizeEvent(e)
        if hasattr(self, "splash_screen"):
            self.splash_screen.resize(self.size())

    def connect_signal_to_slot(self):
        """connect signal to slot"""
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def check_update(self, ignore: bool = False):
        """check software update

        Parameters
        ----------
        ignore: bool
            ignore message box when no updates are available
        """
        if self.version_manager.has_new_version():
            self.show_message_box(
                "Updates available",
                "A new version"
                + f" v{self.version_manager.lastest_version[1:]} "
                + "is available. Do you want to download this version?",
                True,
                lambda: QDesktopServices.openUrl(QUrl(RELEASE_URL)),
            )
        elif not ignore:
            self.show_message_box(
                "No updates available",
                f"{APP_NAME} has been updated to the latest version, feel free to use it.",
            )

    def show_message_box(
        self, title: str, content: str, show_yes_button=False, yesSlot=None
    ):
        """show message box"""
        w = MessageBox(title, content, self)
        if not show_yes_button:
            w.cancelButton.setText("Close")

        if w.exec() and yesSlot is not None:
            yesSlot()
