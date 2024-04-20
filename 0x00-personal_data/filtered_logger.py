#!/usr/bin/env python3

import re

def filter_datum(fields, redaction, message, separator):
    value = message
    value = map(lambda val: re.sub(r'(?<=' + val + r'=)([a-z]+|(\d+/\d+/\d+)?)@?\w+(.com)?', redaction,  value), fields)
    return list(value)[-1]
