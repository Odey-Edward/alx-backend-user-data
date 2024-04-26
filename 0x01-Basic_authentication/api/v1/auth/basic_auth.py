#!/usr/bin/env python3
""" BasicAuth Module """

import base64
from api.v1.auth.auth import Auth


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

        try:
            value = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        return value.decode('utf-8')

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
