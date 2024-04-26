#!/usr/bin/env python3
"""AUTH Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """return hashed password"""

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Auth class initialization method"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            password = _hash_password(password)
            user = self._db.add_user(email, password)

            return user

        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """check for valid user credential"""
        try:
            user = self._db.find_user_by(email=email)
        except (NoResultFound):
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """create new session id for user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return

        id = _generate_uuid()

        self._db.update_user(user.id, session_id=id)

        return id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Find user by session ID"""
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        password = _hash_password(password)

        data = dict(reset_token=None, hashed_password=password)

        self._db.update_user(user.id, **data)
