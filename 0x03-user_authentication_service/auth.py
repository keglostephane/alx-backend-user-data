#!/usr/bin/env python3
"""Auth Module
"""
from db import DB
from user import User
from bcrypt import hashpw, gensalt
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """returns salted hash of input password"""
    if password:
        passwd_bytes = password.encode('utf-8')
        salt = gensalt()
        return hashpw(passwd_bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            passwd = _hash_password(password)
            user = User()
            user.email = email
            user.hashed_password = passwd
            self._db._session.add(user)
            self._db._session.commit()
            return user
        else:
            raise ValueError("User {} already exists".format(user.email))
