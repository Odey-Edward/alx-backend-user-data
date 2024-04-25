#!/usr/bin/env python3
""" Authentication Module """

from flask import request
from typing import TypeVar, List


class Auth:
    """Authentication Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if a route require authentication"""
        if not excluded_paths or not path:
            return True

        if path in excluded_paths:
            return False
        if path + '/' in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header public method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return current user"""
        return None
