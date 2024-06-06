#!/usr/bin/env python3
"""Auth module
"""
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self,
                     path: str,
                     excluded_paths: List[str]) -> bool:
        """paths to authenticate"""
        if path is None or excluded_paths is None:
            return True
        for endpoint in excluded_paths:
            if '*' not in endpoint:
                if endpoint[:-1] == path or endpoint == path:
                    return False
            else:
                if path.startswith(endpoint[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user"""
        return None
