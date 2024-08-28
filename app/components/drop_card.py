# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QApplication,
)

from lib import (
    CardWidget,
    FluentIcon,
    TitleLabel,
    PrimaryPushButton,
)

from ..common.style_sheet import StyleSheet


class DropCard(CardWidget):
    """DropCard"""

    tooltip_signal = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setObjectName("DropCard")

        StyleSheet.DROP_CARD.apply(self)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(12)

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(12)

        self.clipboard = QApplication.clipboard()
        self.init_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.area_label = QLabel("Drag & Drop File(s) Here", self)
        self.area_label.setAlignment(Qt.AlignCenter)
        self.area_label.setObjectName("area_label")

        self.or_label = TitleLabel("or", self)
        self.or_label.setAlignment(Qt.AlignCenter)

        self.select_button = PrimaryPushButton(
            FluentIcon.DICTIONARY_ADD, "Select File(s)", self
        )
        self.select_button.clicked.connect(self.show_file_dialog)

        self.paste_button = PrimaryPushButton(
            FluentIcon.PASTE, "Paste File(s)", self
        )
        self.paste_button.clicked.connect(self.paste_file)

    def init_layout(self):
        """initialize layout"""
        self.main_layout.addWidget(self.area_label)
        self.main_layout.addWidget(self.or_label)
        self.main_layout.addSpacing(10)

        self.button_layout.addWidget(self.select_button)
        self.button_layout.addWidget(self.paste_button)
        self.main_layout.addLayout(self.button_layout)

    def show_file_dialog(self):
        """show file dialog and get files"""
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Files", "")

        if file_paths:
            self.tooltip_signal.emit(
                "success",
                "Files added",
                "Selected files have been added successfully",
            )
            for i in file_paths:
                print(i)

    def paste_file(self):
        """retrieve files copied to clipboard"""
        mime_data = self.clipboard.mimeData()
        if mime_data.hasUrls():
            urls = mime_data.urls()
            file_paths = [url.toLocalFile() for url in urls]
            if file_paths:
                self.tooltip_signal.emit(
                    "success",
                    "Files added",
                    "Selected files have been added successfully",
                )
                for file_path in file_paths:
                    print(file_path)
        else:
            self.tooltip_signal.emit(
                "warning",
                "Files could not be added",
                "No files copied to clipboard",
            )

    def dragEnterEvent(self, event):
        """drag enter event"""
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """drag move event"""
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """drop event"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            urls = event.mimeData().urls()
            file_paths = [url.toLocalFile() for url in urls]

            if file_paths:
                self.tooltip_signal.emit(
                    "success",
                    "Files added",
                    "Selected files have been added successfully",
                )
                for file_path in file_paths:
                    print(file_path)
                event.accept()

        else:
            event.ignore()
