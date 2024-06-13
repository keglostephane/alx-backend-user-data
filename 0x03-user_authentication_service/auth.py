#!/usr/bin/env python3
"""Auth Module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """returns salted hash of input password"""
    if password:
        passwd_bytes = password.encode('utf-8')
        salt = gensalt()
        return hashpw(passwd_bytes, salt)
