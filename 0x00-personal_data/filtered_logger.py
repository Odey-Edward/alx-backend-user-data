#!/usr/bin/env python3
"""filter_datum & RedactingFormatter Module"""
import re
from typing import List
import logging
import mysql.connector
import os

PII_FIELDS = ('email', 'ssn', 'password', 'name', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for v in fields:
        message = re.sub(rf"(?<={v}=).*?{separator}",
                         f"{redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """Create and return a logger"""

    user_data = logging.getLogger('user_data')

    user_data.setLevel(logging.INFO)

    user_data.propagate = False

    handler = logging.StreamHandler()

    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    user_data.addHandler(handler)

    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Implement db conectivity
    """
    psw = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        host=host,
        database=db_name,
        user=username,
        password=psw)
    return conn


def main() -> None:
    """ first method to execute"""
    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    result = cursor.fetchall()

    for row in result:
        print(row)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Class initialization"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """return the redacted logging"""
        result = filter_datum(
                self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        record.msg = result

        return super().format(record)


if __name__ == "__main__":
    main()
