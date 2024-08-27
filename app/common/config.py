# coding:utf-8
import os

from lib import (
    qconfig,
    QConfig,
    OptionsValidator,
    OptionsConfigItem,
)


class Config(QConfig):
    """Config of application"""

    # main window
    dpiScale = OptionsConfigItem(
        "MainWindow",
        "DpiScale",
        "Auto",
        OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
        restart=True,
    )


cfg = Config()
config_path = os.path.join("app", "config", "config.json")
qconfig.load(config_path, cfg)
