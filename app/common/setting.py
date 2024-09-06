# coding: utf-8
from pathlib import Path
from PyQt5.QtCore import QStandardPaths

# about project
YEAR = 2024
AUTHOR = "odest"
VERSION = "v1.0.0"
APP_NAME = "DonkeyDoc"
RELEASE_URL = "https://github.com/odest/DonkeyDoc/releases/latest"
API_URL = "https://api.github.com/repos/odest/DonkeyDoc/releases/latest"

# about config
CONFIG_FOLDER = (
    Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
    / APP_NAME
)
CONFIG_FILE = CONFIG_FOLDER / "config.json"

# about files
SUPPORT_IMG_FORMAT = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".svg")
SUPPORT_FORMAT = (
    ".pdf",
    ".epub",
    ".txt",
    ".mobi",
    ".xps",
    ".fb2",
    ".cbz",
) + SUPPORT_IMG_FORMAT
