#!/usr/bin/env python3
"""encrypt_password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """return Encrypted passwords"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hash_password: bytes, password: str) -> bool:
    """Check valid password"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)
