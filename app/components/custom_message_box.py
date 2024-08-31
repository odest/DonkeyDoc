# coding:utf-8

import os
from typing import Any, Dict

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from lib import (
    FluentIcon,
    CaptionLabel,
    SubtitleLabel,
    MessageBoxBase,
    StrongBodyLabel,
    PasswordLineEdit,
    HorizontalSeparator,
    TransparentToolButton,
)


class PasswordMessageBox(MessageBoxBase):
    """Password message box"""

    def __init__(self, password, is_incorrect, parent=None):
        super().__init__(parent)

        # init widget
        self.title_label = SubtitleLabel("This File is Encrypted", self)
        self.line_edit = PasswordLineEdit(self)
        self.line_edit.setPlaceholderText("Enter the file password")
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.setText(password)

        self.caption_label = CaptionLabel("Incorrect Password!", self)
        self.caption_label.setTextColor(QColor(255, 0, 0), QColor(255, 0, 0))
        self.caption_label.setVisible(is_incorrect)

        # add widget to view layout
        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.line_edit)
        self.viewLayout.addWidget(self.caption_label)

        # change the text of button
        self.yesButton.setText("Authenticate")
        self.cancelButton.setText("Cancel")

        self.widget.setMinimumWidth(360)

    def get_password(self):
        """get password"""
        return self.line_edit.text()


class InfoDialogBox(MessageBoxBase):
    """Info Dialog Box"""

    def __init__(self, path, doc, parent=None):
        super().__init__(parent)

        self.path = path
        self.document = doc

        self.viewLayout.setContentsMargins(24, 16, 24, 24)
        self.cancelButton.setText("Close")
        self.hideYesButton()

        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setSpacing(12)

        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(32)

        self.key_layout = QVBoxLayout()
        self.key_layout.setContentsMargins(0, 0, 0, 0)
        self.key_layout.setSpacing(12)

        self.value_layout = QVBoxLayout()
        self.value_layout.setContentsMargins(0, 0, 0, 0)
        self.value_layout.setSpacing(12)

        self.init_widget()
        self.init_layout()

    def init_widget(self):
        """initialize widget"""
        self.title_label = SubtitleLabel("File Informations", self)

        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)
        self.close_button.clicked.connect(self.on_close_button_clicked)

        for key, value in self.get_information().items():
            label_1 = StrongBodyLabel(f"{key}:", self)
            self.key_layout.addWidget(label_1)
            label_2 = CaptionLabel(str(value), self)
            self.value_layout.addWidget(label_2)

            if key == "Page Count":
                sep1 = HorizontalSeparator(self)
                sep2 = HorizontalSeparator(self)
                self.key_layout.addWidget(sep1)
                self.value_layout.addWidget(sep2)

    def init_layout(self):
        """initialize layout"""
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.close_button)
        self.viewLayout.addLayout(self.title_layout)
        self.viewLayout.addSpacing(12)

        self.content_layout.addLayout(self.key_layout)
        self.content_layout.addStretch()
        self.content_layout.addLayout(self.value_layout)
        self.viewLayout.addLayout(self.content_layout)

    def get_information(self) -> Dict[str, Any]:
        """get information"""
        metadata = self.document.metadata
        information = {
            "File Name": os.path.basename(self.path),
            "File Path": self.path,
            "File Format": metadata["format"],
            "File Size": os.path.getsize(self.path),
            "Page Count": self.document.page_count,
            "Title": metadata["title"],
            "Author": metadata["author"],
            "Creator": metadata["creator"],
            "Producer": metadata["producer"],
            "Subject": metadata["subject"],
            "Keywords": metadata["keywords"],
            "Encryption": metadata["encryption"],
            "Creation Date": metadata["creationDate"],
            "Modification Date": metadata["modDate"],
        }
        return information

    def on_close_button_clicked(self):
        """on close button clicked"""
        self.reject()
