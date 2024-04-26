#!/usr/bin/env python3
""" BasicAuth Module """

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
