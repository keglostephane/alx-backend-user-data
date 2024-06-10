#!/usr/bin/env python3
"""User Session
"""
from .base import Base


class UserSession(Base):
    """Implement User Session in Database.
    """
    def __init__(self, *args: list, **kwargs: dict):
        """Initializer"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
