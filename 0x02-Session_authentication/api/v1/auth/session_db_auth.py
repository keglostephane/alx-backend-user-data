#!/usr/bin/env python3
"""Session Database with Expiration
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime
from typing import Union


class SessionDBAuth(SessionExpAuth):
    """Session Database Expiration
    """

    def create_session(self, user_id=None) -> Union[bool, str]:
        """create a user session"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        user_session_id = UserSession(user_id=user_id, session_id=session_id)
        user_session_id.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> Union[bool, str]:
        """Return user ID from from session_id of UserSession.
        """
        if not session_id:
            return None

        user_sessions = UserSession.search({'session_id': session_id})

        if not user_sessions:
            return None

        user_session = user_sessions[0]

        if not self.session_duration:
            return user_session.user_id
        if user_session.created_at + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """Terminate user session.
        """
        session_id = self.session_cookie(request)
        user_sessions = UserSession.search({'session_id': session_id})

        if request is None:
            return False
        if not session_id:
            return False
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()

        return True
