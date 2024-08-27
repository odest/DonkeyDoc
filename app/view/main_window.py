# coding: utf-8
import os

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from lib import FluentWindow, SplashScreen, FluentIcon
from app.view.home_interface import HomeInterface


class MainWindow(FluentWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.init_window()
        self.init_interface()
        self.init_navigation()
        self.splash_screen.finish()

    def init_interface(self):
        """Initialize the interfaces"""
        self.home_interface = HomeInterface(self)

    def init_navigation(self):
        """Add navigation items"""
        self.addSubInterface(self.home_interface, FluentIcon.HOME, "Home")

    def init_window(self):
        """Initialize the main window properties and display the splash screen."""
        self.resize(970, 790)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(os.path.join("docs", "logo.svg")))
        self.setWindowTitle("DonkeyDoc")

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
