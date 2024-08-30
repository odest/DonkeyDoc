# coding:utf-8
import os
from pymupdf import Document
from typing import Optional, Tuple

SUPPORT_IMG_FORMAT = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".svg")
SUPPORT_FORMAT = (
    ".pdf",
    ".epub",
    ".mobi",
    ".xps",
    ".fb2",
    ".cbz",
) + SUPPORT_IMG_FORMAT


class Doc(Document):
    """
    A wrapper around the fitz.Document class with optional password handling.
    """

    password: Optional[str] = None


def validate_file(file_path: str) -> Tuple[bool, str, str, str]:
    """
    Validates the given file path by checking if the file exists, if its extension is supported,
    and if it can be opened. Also checks if the file requires a password.

    Args:
        file_path (str): The path to the file to be validated.

    Returns:
        Tuple[bool, str, str, str]: A tuple where:
            - A boolean indicating if the file is valid.
            - A status string ("success", "warning", or "error").
            - A title for a tool tip.
            - A content message for a tool tip.
    """
    if not os.path.isfile(file_path):
        return (
            False,
            "warning",
            "File could not be opened",
            "This is not a file, it's a folder.",
        )

    file_name = os.path.basename(file_path)

    if not file_name.endswith(SUPPORT_FORMAT):
        return (
            False,
            "warning",
            "File could not be opened",
            "Unsupported file type.",
        )

    try:
        doc = Doc(filename=file_path)
        doc.password = None
    except RuntimeError:
        return (
            False,
            "error",
            "File could not be opened",
            "File is not suitable or is corrupted.",
        )

    if doc.needs_pass:
        return (
            False,
            "warning",
            "File could not be opened",
            "File is password protected.",
        )

    return (
        True,
        "success",
        "File opened",
        "File have been opened successfully.",
    )
