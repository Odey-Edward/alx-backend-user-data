#!/usr/bin/env python3
"""AUTH Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import uuid


def _hash_password(password):
    """return hashed password"""

    password_bytes = password.encode('utf-8')

    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def _generate_uuid():
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


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

    def create_session(self, email) -> str:
        """create new session id for user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return

        id = _generate_uuid()

        user.session_id = id

        session = self._db._session

        session.commit()

        return id
