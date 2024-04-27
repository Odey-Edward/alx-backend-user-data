#!/usr/bin/env python3
"""encrypt_password module"""
import bcrypt


def hash_password(password: str) -> str:
    """return Encrypted passwords"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
