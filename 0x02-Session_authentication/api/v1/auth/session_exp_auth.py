#!/usr/bin/env python3
"""Session With Expiration
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from typing import TypeVar, Union
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session with date expiration.
    """
    session_dictionary = {}

    def __init__(self) -> TypeVar('SessionExpAuth'):
        """initializer"""
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None) -> Union[None, str]:
        """ Create a user session.
        """
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = self.session_dictionary
        self.session_dictionary["user_id"] = user_id
        self.session_dictionary["created_at"] = datetime.now()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Returns user id from session id.
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        if not self.session_duration:
            return self.session_dictionary.get("user_id")
        if not self.session_dictionary.get("created_at"):
            return None
        if self.session_dictionary.get("created_at") + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return self.session_dictionary.get("user_id")
