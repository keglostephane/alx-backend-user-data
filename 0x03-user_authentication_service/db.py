#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User
from typing import Dict, Union


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

    def add_user(self, email: str, hashed_password: str) -> User:
        """Save user to database
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Retrieve the first user matching keyword argument"""
        if not kwargs:
            raise InvalidRequestError

        try:
            user = self._session.query(User).filter_by(**kwargs)
        except AttributeError:
            raise InvalidRequestError

        return user
