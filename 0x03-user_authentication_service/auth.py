#!/usr/bin/env python3
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password):
    """return hashed password"""

    password_bytes = password.encode('utf-8')

    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Auth class initialization method"""
        self._db = DB()

    def register_user(self, email, password):
        """register a user"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            password = _hash_password(password)
            user = self._db.add_user(email, password)

            return user

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email, password):
        """check for valid user credential"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
