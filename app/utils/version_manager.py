# coding: utf-8
import re
import requests

from PyQt5.QtCore import QVersionNumber
from ..common.setting import VERSION, API_URL


class VersionManager:
    """Version manager"""

    def __init__(self):
        self.current_version = VERSION
        self.lastest_version = VERSION
        self.version_pattern = re.compile(r"v(\d+)\.(\d+)\.(\d+)")

    def get_latest_version(self):
        """get latest version"""
        try:
            response = requests.get(API_URL, timeout=2)
            response.raise_for_status()
            if response.status_code == 200:
                # parse version
                version = response.json()["tag_name"]  # type:str
                match = self.version_pattern.search(version)
                if not match:
                    return VERSION
                self.lastest_version = version
                return version
        except requests.ConnectionError:
            return VERSION
        except requests.Timeout:
            return VERSION
        return VERSION

    def has_new_version(self):
        """check whether there is a new version"""
        version = QVersionNumber.fromString(self.get_latest_version()[1:])[0]
        current_version = QVersionNumber.fromString(self.current_version[1:])[
            0
        ]
        return version > current_version
