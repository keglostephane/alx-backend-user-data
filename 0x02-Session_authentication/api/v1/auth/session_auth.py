#!/usr/bin/env python3
"""Session
"""
from .auth import Auth
from uuid import uuid4
from typing import TypeVar, NoReturn
from models.user import User


class SessionAuth(Auth):
    """Not implemented
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user ID based on his session ID.
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Get user from a cookie value.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None) -> NoReturn:
        """Destroy user session (logout).
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if request is None:
            return False
        if not session_id:
            return False
        if not user_id:
            return False
        if not User.get(user_id):
            return False

        user_session_ids = [key for key in self.user_id_by_session_id.keys()
                            if self.user_id_by_session_id[key] == user_id]

        for session_id in user_session_ids:
            del self.user_id_by_session_id[session_id]

        return True
