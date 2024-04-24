#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound

from user import Base, User

VALID_FIELDS = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """create and add new user to the database"""

        user = User()

        user.email = email
        user.hashed_password = hashed_password

        session_s = self._session

        session_s.add(user)
        session_s.commit()

        return user

    def find_user_by(self, **kwargs):
        """find user filtered by the parameters passed"""

        if not kwargs or any(k not in VALID_FIELDS for k in kwargs):
            raise InvalidRequestError

        session = self._session

        result = session.query(User).filter_by(**kwargs).one()

        if not result:
            raise NoResultFound

        return result

    def update_user(self, user_id, **kwargs):
        """update User user object"""
        user = self.find_user_by(id=user_id)

        session = self._session

        if user:
            for k, v in kwargs.items():
                if not hasattr(user, k):
                    raise ValueError
                setattr(user, k, v)
            session.commit()
