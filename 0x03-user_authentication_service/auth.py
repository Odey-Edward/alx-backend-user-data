#!/usr/bin/env python3
import bcrypt


def _hash_password(password):
    """return hashed password"""

    password_bytes = password.encode('utf-8')

    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())
