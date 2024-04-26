#!/usr/bin/env python3
"""AUTH Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import uuid
from typing import ByteString


def _hash_password(password: str) -> ByteString:
    """return hashed password"""

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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

        self._db.update_user(user.id, session_id=id)

        return id

    def get_user_from_session_id(self, session_id):
        """Find user by session ID"""
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id):
        """Destroy session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email):
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token, password):
        """ Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        password = _hash_password(password)

        data = dict(reset_token=None, hashed_password=password)

        self._db.update_user(user.id, **data)
