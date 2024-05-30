#!/usr/bin/env python3
"""filter_datum
"""
import logging
import re
from typing import List, Tuple


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Retuns the log message obfuscated"""
    pattern = '|'.join([rf'(?<={field}=)[^{separator}]+' for field in fields])
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str] = None):
        """Initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter value in log records"""
        record.message = filter_datum(self.fields, self.REDACTION,
                                      super().format(record),
                                      self.SEPARATOR)
        return record.message
