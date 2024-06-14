#!/usr/bin/env python3
"""Auth Module
"""
from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Return the user for a given session.
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session.
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        return self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Update user reset token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, reset_token=_generate_uuid())

        return user.reset_token
