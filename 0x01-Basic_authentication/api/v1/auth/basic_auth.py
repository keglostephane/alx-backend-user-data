#!/usr/bin/env python3
"""Basic Authentication
"""
import binascii
from .auth import Auth
from models.user import User
from base64 import b64decode
from typing import TypeVar


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        return decoded.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Returns user email and password from Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_email, str):
            return None
        try:
            User.load_from_file()
            users = User.all()
            if not len(users):
                return None
            else:
                user_list = User.search({'email': user_email})
                if not user_list:
                    return None
                if not user_list[0].is_valid_password(user_pwd):
                    return None
        except FileNotFoundError:
            return None
        else:
            return user_list[0]
