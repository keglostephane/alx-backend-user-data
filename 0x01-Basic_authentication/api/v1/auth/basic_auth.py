#!/usr/bin/env python3
"""Basic Authentication
"""
from .auth import Auth


class BasicAuth(Auth):
    """a Basic Authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns Base64 part of Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split()[1]
