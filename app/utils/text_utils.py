# coding:utf-8

import re

from enum import Enum
from datetime import datetime, timedelta, timezone


class DateFormat(Enum):
    """
    Enum class for defining various date formats and their associated parsing details.
    Each member represents a specific date format, including its regex pattern,
        date format string, and timezone type.
    """

    D_OFFSET = (r"D:(\d{14})([+\-]\d{2}'\d{2})", "%Y%m%d%H%M%S", "offset")
    D_UTC = (r"D:(\d{14})Z", "%Y%m%d%H%M%S", "utc")
    OFFSET = (r"(\d{14})([+\-]\d{2}'\d{2})", "%Y%m%d%H%M%S", "offset")
    UTC = (r"(\d{14})Z", "%Y%m%d%H%M%S", "utc")
    OFFSET_ISO = (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})([+\-]\d{2}:\d{2})",
        "%Y-%m-%dT%H:%M:%S",
        "offset",
    )
    ISO_UTC = (
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z",
        "%Y-%m-%dT%H:%M:%S",
        "utc",
    )
    SHORT_DATE = (r"D:(\d{8})", "%Y%m%d", "utc")
    SHORT_DATE_ALT = (r"(\d{7})", "%Y%j", "utc")


def parse_date(date_str: str) -> str:
    """
    Parses a date string into a human-readable format.

    This function supports multiple date formats and timezone representations:
    - `D:YYYYMMDDHHMMSS±HH'MM'`
    - `D:YYYYMMDDHHMMSSZ`
    - `YYYYMMDDHHMMSS±HH'MM'`
    - `YYYYMMDDHHMMSSZ`
    - `YYYY-MM-DDTHH:MM:SS±HH:MM`
    - `YYYY-MM-DDTHH:MM:SSZ`
    - `D:YYYYMMDD`
    - `YYYYDDD`

    Args:
        date_str (str): The date string to be parsed. It can be in various formats as listed above.

    Returns:
        str: The parsed date in the format "dd.mm.yyyy HH:MM:SS".
            If the input string doesn't match any supported format, returns the original string.
    """
    for date_format in DateFormat:
        pattern, date_format_str, tz_type = date_format.value
        match = re.match(pattern, date_str)
        if match:
            date_part = match.group(1)
            tz_part = match.group(2) if len(match.groups()) > 1 else None

            try:
                if date_format_str == "%Y%j":  # Handle Julian date format
                    date_obj = datetime.strptime(date_part, date_format_str)
                else:
                    date_obj = datetime.strptime(date_part, date_format_str)
            except ValueError:
                continue  # If parsing fails, try the next format

            if tz_type == "offset":
                if tz_part:
                    offset_hours = int(tz_part[:3])
                    offset_minutes = int(tz_part[4:])
                    offset = timedelta(
                        hours=offset_hours, minutes=offset_minutes
                    )
                    date_obj -= offset

            elif tz_type == "utc":
                date_obj = date_obj.replace(tzinfo=timezone.utc)

            return date_obj.strftime("%d.%m.%Y %H:%M:%S")

    # If no format matches, returns the original string.
    return date_str


def truncate_text(text: str, max_length: int, ellipsis: str = "...") -> str:
    """
    Truncates a string to a specified maximum length and appends an ellipsis if necessary.

    Args:
        text (str): The input string that may need to be truncated.
        max_length (int): The maximum allowed length of the string.
                            If the input string exceeds this length, it will be truncated.
        ellipsis (str): The string to append if the text is truncated.
                            Default is "..." but can be customized.

    Returns:
        str: The truncated string, ending with `ellipsis` if the original string was
            longer than `max_length`.
            If the original string is within the allowed length, it is returned unchanged.

    Raises:
        ValueError: If `max_length` is less than or equal to the length of `ellipsis`,
                    or if `max_length` is negative.
    """
    if max_length < 0:
        raise ValueError("Maximum length must be a non-negative integer.")

    if len(ellipsis) >= max_length:
        raise ValueError(
            "Maximum length must be greater than the length of the ellipsis."
        )

    if len(text) > max_length:
        truncated_text = text[: max_length - len(ellipsis)] + ellipsis
    else:
        truncated_text = text

    return truncated_text
