#!/usr/bin/env python3
""" BasicAuth Module """

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authentication Class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extract the basic authorization value
        """
        if not authorization_header:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.replace('Basic ', '')

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Base64 decode Basic Authorization Value
        """
        if not base64_authorization_header:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        b64_auth_header = base64_authorization_header

        try:
            decoded_value = base64.b64decode(b64_auth_header).decode('utf-8')
            return decoded_value
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if not decoded_base64_authorization_header:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        value = decoded_base64_authorization_header.split(':')

        return value[0], value[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        try:

            users = User.search({'email': user_email})

            if not users or users == []:
                return None

            for user in users:
                if user.is_valid_password(user_pwd):
                    return user

            return None

        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrive current with Basic Authorization"""
        auth_header = self.authorization_header(request)

        if auth_header:
            auth_value = self.extract_base64_authorization_header(auth_header)

            if auth_value:
                decoded_value = self.decode_base64_authorization_header(
                        auth_value)

                if decoded_value:
                    user_data = self.extract_user_credentials(decoded_value)

                    if user_data:
                        user = self.user_object_from_credentials(
                                user_data[0], user_data[1])

                        if user:
                            return user
        return None
