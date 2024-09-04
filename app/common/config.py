# coding:utf-8
import os
import sys

from lib import (
    qconfig,
    QConfig,
    ConfigItem,
    BoolValidator,
    OptionsValidator,
    OptionsConfigItem,
)


def is_win_11():
    """is Windows 11

    Returns:
        bool: if platform is windows11 return True
    """
    return sys.platform == "win32" and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """Config of application"""

    # main window
    micaEnabled = ConfigItem(
        "MainWindow", "MicaEnabled", is_win_11(), BoolValidator()
    )
    dpiScale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )


USER_HOME = os.path.expanduser("~")
APP_HOME = os.path.join(USER_HOME, ".DonkeyDoc")
CONFIG_PATH = os.path.join(APP_HOME, "config", "config.json")

cfg = Config()
qconfig.load(CONFIG_PATH, cfg)
