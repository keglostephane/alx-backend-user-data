#!/usr/bin/env python3
"""filter_datum
"""
import logging
import re
import mysql.connector
from typing import List
from os import environ


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Retuns the log message obfuscated"""
    pattern = '|'.join([rf'(?<={field}=)[^{separator}]+' for field in fields])
    return re.sub(pattern, redaction, message)


def get_logger() -> logging.Logger:
    """Returns a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ initiate connection to a database.
    """
    db_host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    db_user = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    try:
        connection = mysql.connector.connection.MySQLConnection(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_pwd,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        raise Exception(err)


def main():
    """Logs the information about user records in a table.
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, msg, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = []):
        """Initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter value in log records"""
        record.message = filter_datum(self.fields, self.REDACTION,
                                      super().format(record),
                                      self.SEPARATOR)
        return record.message


if __name__ == "__main__":
    main()
