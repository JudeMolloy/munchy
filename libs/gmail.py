# GMAIL OAuth2
import os
import requests

from oauthlib.oauth2 import WebApplicationClient


class Gmail:
    # Configuration
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    # OAuth 2 client setup
    googleClient = WebApplicationClient(GOOGLE_CLIENT_ID)

    @classmethod
    def get_google_provider_cfg(cls):
        return requests.get(cls.GOOGLE_DISCOVERY_URL).json()
