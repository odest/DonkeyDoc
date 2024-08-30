# coding:utf-8
from PyQt5.QtGui import QColor
from lib import MessageBoxBase, SubtitleLabel, PasswordLineEdit, CaptionLabel


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
