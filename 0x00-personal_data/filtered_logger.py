#!/usr/bin/env python3
import re


def filter_datum(fields, redaction, meg, separator):
    """returns the log message obfuscated"""
    for val in fields:
        meg = re.sub(r'(?<=' + val + r'=)([a-z]+|(\d+/\d+/\d+)?)@?\w+(.com)?',
                     redaction,  meg)
    return message
