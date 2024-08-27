# coding: utf-8
import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication

from lib import FluentWindow, SplashScreen
from app.common.config import cfg


class MainWindow(FluentWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.init_window()
        self.splash_screen.finish()

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


if __name__ == "__main__":
    # enable dpi scale
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # create main window
    w = MainWindow()
    w.show()

    app.exec_()
