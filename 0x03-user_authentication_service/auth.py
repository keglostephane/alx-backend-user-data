#!/usr/bin/env python3
"""Auth Module
"""
from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """returns salted hash of input password"""
    if password:
        passwd_bytes = password.encode('utf-8')
        salt = gensalt()
        return hashpw(passwd_bytes, salt)


def _generate_uuid() -> str:
    """Generate a new UUID.
    """
    return str(uuid4())


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
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError("User {} already exists".format(user.email))

    def valid_login(self, email: str, password: str) -> bool:
        """Authenticate user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """create a session and return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=_generate_uuid())
        except NoResultFound:
            return None

        return user.session_id
