#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for v in fields:
        message = re.sub(rf"(?<={v}=).*?{separator}",
                         f"{redaction}{separator}", message)
    return message
