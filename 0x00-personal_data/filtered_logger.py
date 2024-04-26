#!/usr/bin/env python3
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 meg: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for val in fields:
        meg = re.sub(r'(?<=' + val + r'=)([a-z]+|(\d+/\d+/\d+)?)@?\w+(.com)?',
                     redaction,  meg)
    return meg
