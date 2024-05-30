#!/usr/bin/env python3
"""filter_datum
"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Retuns the log message obfuscated"""
    pattern = '|'.join([rf'(?<={field}=)[^{separator}]+' for field in fields])
    return re.sub(pattern, 'xxx', message)
