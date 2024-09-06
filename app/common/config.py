# coding:utf-8
import sys

from lib import (
    qconfig,
    QConfig,
    ConfigItem,
    BoolValidator,
    OptionsValidator,
    OptionsConfigItem,
)

from .setting import CONFIG_FILE


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

    # software update
    checkUpdateAtStartUp = ConfigItem(
        "Update", "CheckUpdateAtStartUp", True, BoolValidator()
    )


cfg = Config()
qconfig.load(CONFIG_FILE, cfg)
