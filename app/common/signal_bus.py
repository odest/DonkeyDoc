# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """Signal bus"""

    micaEnableChanged = pyqtSignal(bool)


signalBus = SignalBus()
