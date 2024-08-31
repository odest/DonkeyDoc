# coding:utf-8
import os
import math

from typing import Any, Dict
from pymupdf import Document

from ..utils.text_utils import truncate_text, parse_date


def get_information(path: str, document: Document) -> Dict[str, Any]:
    """
    Extracts and returns metadata and file information from a PDF document.

    Args:
        path (str): The file path to the document.
        document (Document): An instance of the `Document` class from pymupdf, representing the document.

    Returns:
        Dict[str, Any]: A dictionary containing the metadata and file information.
    """
    metadata = document.metadata
    information = {
        "File Name": truncate_text(os.path.basename(path), 50),
        "File Path": truncate_text(os.path.dirname(path), 50),
        "File Format": metadata["format"],
        "File Size": get_file_size(path),
        "Page Count": document.page_count,
        "Title": truncate_text(metadata["title"], 50),
        "Author": truncate_text(metadata["author"], 50),
        "Creator": truncate_text(metadata["creator"], 50),
        "Producer": truncate_text(metadata["producer"], 50),
        "Subject": truncate_text(metadata["subject"], 50),
        "Keywords": truncate_text(metadata["keywords"], 50),
        "Encryption": metadata["encryption"],
        "Creation Date": parse_date(metadata["creationDate"]),
        "Modification Date": parse_date(metadata["modDate"]),
    }
    return information


def get_file_size(path: str) -> str:
    """
    Calculates the human-readable size of a file.

    Args:
        path (str): The file path for which the size needs to be calculated.

    Returns:
        str: The size of the file in a human-readable format, such as "10.23 MB" or "512 B".
            The size is formatted with the appropriate unit (bytes, kilobytes, megabytes, etc.)
            and rounded to two decimal places for clarity.
    """
    size_bytes = os.path.getsize(path)

    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
